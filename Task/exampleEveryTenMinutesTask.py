#expresion_cron=*/10 * * * *
"""
FelipdelosH - 2023

NOTE: the time is configurate in main.py (registration)

This save it´s only for test a project CronJobsByLOko
"""
with open("tenMinuteFile.txt", "w") as f:
    f.write("EVERY TEN MINUTES I WRITE THIS FILE")