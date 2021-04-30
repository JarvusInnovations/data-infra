# ---
# python_callable: main
# provide_context: true
# dependencies:
#   - valid_agency_paths
#   - wait_for_external_tables
# ---

"""
Process and dump files for gtfs_schedule_history.calitp_files external table.
This is for the files downloaded for an agency, as well as validator results.
"""

from calitp import read_gcfs, get_bucket, save_to_gcfs
import pandas as pd
import gcsfs


def main(execution_date, **kwargs):
    # TODO: remove hard-coded project string
    fs = gcsfs.GCSFileSystem(project="cal-itp-data-infra")

    bucket = get_bucket()

    f = read_gcfs(f"schedule/{execution_date}/status.csv")
    status = pd.read_csv(f)

    success = status[lambda d: d.status == "success"]

    gtfs_file = []
    for ii, row in success.iterrows():
        agency_folder = f"{row.itp_id}_{row.url_number}"
        agency_url = f"{bucket}/schedule/{execution_date}/{agency_folder}"

        dir_files = [x for x in fs.listdir(agency_url) if x["type"] == "file"]

        for x in dir_files:
            gtfs_file.append(
                {
                    "calitp_itp_id": row["itp_id"],
                    "calitp_url_number": row["url_number"],
                    "calitp_extracted_at": execution_date.to_date_string(),
                    "full_path": x["name"],
                    "name": x["name"].split("/")[-1],
                    "size": x["size"],
                    "md5_hash": x["md5Hash"],
                }
            )

    res = pd.DataFrame(gtfs_file)

    save_to_gcfs(
        res.to_csv(index=False).encode(),
        f"schedule/{execution_date}/processed/files.csv",
        use_pipe=True,
    )
