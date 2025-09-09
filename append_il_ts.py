import pandas as pd
from pathlib import Path
import re

BASE = Path(__file__).parent
IL_TS_DIR = BASE / 'IL_TS'
MASTER_DETAILED = BASE / 'master_database_detailed.csv'
MASTER_PIVOT = BASE / 'master_database_pivot.csv'
MASTER_SUMMARY = BASE / 'master_database_summary.csv'

# Map filenames (or implied IDs) to topic IDs and names
TOPIC_MAP = {
    6: 'Ionic Liquids (All)',
    7: 'ILs in Electrochemistry',
    8: 'ILs in Electrochemical Manufacturing',
    9: 'Elevated-T IL Electrochemical Manufacturing'
}


def parse_il_ts_file(path: Path):
    """Parse a text file with columns: Publication Years\tRecord Count\t% ..."""
    lines = path.read_text().strip().splitlines()
    rows = []
    # skip header until we find a line that starts with a year (4 digits) or a number
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^(\d{4}|\d{3}|\d{2}|\d{1})\t', line):
            parts = line.split('\t')
            if len(parts) >= 2:
                year = parts[0]
                try:
                    year_i = int(year)
                except ValueError:
                    continue
                try:
                    count = int(parts[1])
                except ValueError:
                    continue
                rows.append((year_i, count))
        else:
            # also handle space separated
            m = re.match(r'^(\d{4}|\d{3}|\d{2}|\d{1})\s+(\d+)', line)
            if m:
                year_i = int(m.group(1))
                count = int(m.group(2))
                rows.append((year_i, count))
    return rows


def main():
    # Backup original master
    if MASTER_DETAILED.exists():
        MASTER_DETAILED.with_suffix('.csv.bak').write_bytes(MASTER_DETAILED.read_bytes())

    df_master = pd.read_csv(MASTER_DETAILED)

    # We'll append TS rows for topics 6-9
    appended_rows = []
    for topic_id in sorted(TOPIC_MAP.keys()):
        fname = f"{topic_id}_" + '_'.join(re.sub(r'[^a-z0-9]+','_', TOPIC_MAP[topic_id].lower()).split('_')[:6]) + '.txt'
        # but files have specific names, just try to find any file starting with f"{topic_id}_"
        candidates = list(IL_TS_DIR.glob(f"{topic_id}_*.txt"))
        if not candidates:
            print(f"No file found for topic {topic_id}")
            continue
        path = candidates[0]
        rows = parse_il_ts_file(path)
        for year, count in rows:
            appended_rows.append({
                'Year': year,
                'Search_Topic_ID': topic_id,
                'Search_Topic': TOPIC_MAP[topic_id],
                'Search_Level': 'TS',
                'Search_Level_Description': 'Title + Abstract + Keywords',
                'Record_Count': count
            })

    if appended_rows:
        df_new = pd.DataFrame(appended_rows)
        # remove existing overlapping TS rows for these topics to avoid duplicates
        mask = ~((df_master['Search_Topic_ID'].isin(TOPIC_MAP.keys())) & (df_master['Search_Level'] == 'TS'))
        df_master_clean = df_master[mask].copy()
        df_combined = pd.concat([df_master_clean, df_new], ignore_index=True, sort=False)
        df_combined = df_combined.sort_values(['Search_Topic_ID','Search_Level','Year'])
        df_combined.to_csv(MASTER_DETAILED, index=False)
        print(f"Appended {len(df_new)} rows to {MASTER_DETAILED}")

        # regenerate pivot
        pivot = df_combined.pivot_table(index=['Year','Search_Topic_ID','Search_Topic'], columns='Search_Level', values='Record_Count', aggfunc='sum', fill_value=0).reset_index()
        pivot_cols = ['Year','Search_Topic_ID','Search_Topic'] + [c for c in ['KW','TI','TS'] if c in pivot.columns]
        pivot = pivot[pivot_cols]
        pivot.to_csv(MASTER_PIVOT, index=False)
        print(f"Wrote pivot to {MASTER_PIVOT}")

        # summary
        summary = df_combined.groupby(['Search_Topic_ID','Search_Topic','Search_Level'], as_index=False)['Record_Count'].sum()
        summary.to_csv(MASTER_SUMMARY, index=False)
        print(f"Wrote summary to {MASTER_SUMMARY}")
    else:
        print("No rows appended.")

if __name__ == '__main__':
    main()
