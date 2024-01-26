BATCH_SUCCESS_SUBJECT = (
    "[CATAPULT] {manifest_group} {manifest_type} BATCH {batch_number} WAS SUCCESSFUL"
)
BATCH_FAIL_SUBJECT = (
    "[CATAPULT] {manifest_group} {manifest_type} BATCH {batch_number} FAILED"
)


########
# BODY #
########


FAILURE_CATAPULT_BODY = """
<HTML>
    <head></head>
    <body>
        <p>bhaou_catapult encountered issues when processing this batch. Attach
        is a CSV with the list of issues </p> <br>
        <br></p>

        <i> This is an automated message, please do not reply. </i>
</body>
</HTML>
"""

SUCCESS_CATAPULT_BODY = """
<HTML>
    <head></head>
    <body>
        <p>bhaou_catapult has successfully process the new batch.
        A manifest was generated and/or sample data uploaded.</p> <br>

        <i> This is an automated message, please do not reply. </i>
</body>
</HTML>
"""
