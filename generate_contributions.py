import os
import sys
import subprocess
import random
from datetime import datetime, timedelta

# Fix Windows console stdout encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_git_cmd(args, env=None):
    result = subprocess.run(["git"] + args, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Git error: {result.stderr.strip()}")
        return False
    return True

def generate_contributions(total_target_commits=735, days=365):
    """
    Generates backdated git commits over the last `days` to boost GitHub profile contributions.
    """
    print(f"[+] Starting contribution generator...")
    print(f"[*] Target commits: {total_target_commits} over the past {days} days\n")

    # Get current git config email/name or set default fallback
    git_email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True).stdout.strip()
    git_name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()

    if not git_email:
        git_email = "shivamgoyal1217@gmail.com"
        run_git_cmd(["config", "user.email", git_email])
    if not git_name:
        git_name = "Shivam Goel"
        run_git_cmd(["config", "user.name", git_name])

    print(f"[*] Git User: {git_name} <{git_email}>")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Distribute commits across days (giving ~260 active days out of 365, ~2 to 5 commits per active day)
    active_days = sorted(random.sample(range(1, days), 260))
    
    # Calculate commit counts for each active day
    commits_per_day = {}
    remaining_commits = total_target_commits
    
    for idx, day_offset in enumerate(active_days):
        if idx == len(active_days) - 1:
            count = remaining_commits
        else:
            count = random.randint(1, 4)
            if remaining_commits - count < (len(active_days) - idx - 1):
                count = 1
        commits_per_day[day_offset] = count
        remaining_commits -= count
        if remaining_commits <= 0:
            break

    dummy_file = "contributions_log.txt"
    created_count = 0

    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = git_name
    env["GIT_AUTHOR_EMAIL"] = git_email
    env["GIT_COMMITTER_NAME"] = git_name
    env["GIT_COMMITTER_EMAIL"] = git_email

    for day_offset, count in commits_per_day.items():
        commit_date_base = start_date + timedelta(days=day_offset)
        
        for c in range(count):
            # Randomize time during standard coding hours (09:00 - 23:00)
            hour = random.randint(9, 22)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_dt = commit_date_base.replace(hour=hour, minute=minute, second=second)
            formatted_date = commit_dt.strftime("%Y-%m-%dT%H:%M:%S")

            with open(dummy_file, "a") as f:
                f.write(f"Contribution entry #{created_count + 1} on {formatted_date}\n")

            run_git_cmd(["add", dummy_file])

            env["GIT_AUTHOR_DATE"] = formatted_date
            env["GIT_COMMITTER_DATE"] = formatted_date

            msg = f"Update feature activity log ({formatted_date})"
            if run_git_cmd(["commit", "-m", msg], env=env):
                created_count += 1

    print(f"\n[Success] Generated {created_count} backdated commits successfully!")
    print("Next Step: Push these commits to GitHub by running:")
    print("   git push origin main")

if __name__ == "__main__":
    generate_contributions()
