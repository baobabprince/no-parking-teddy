# 🟡⚫ Beitar Jerusalem Calendar Sync

> An automation that syncs Beitar Jerusalem's home games at Teddy Stadium to a Google Calendar - so you won't forget to move your car!

[![Sync Calendar](https://github.com/YOUR_USERNAME/beitar-calendar-sync/actions/workflows/sync-calendar.yml/badge.svg)](https://github.com/YOUR_USERNAME/beitar-calendar-sync/actions/workflows/sync-calendar.yml)

## 📖 What does it do?

1.  🕷️ **Scrapes** the Beitar Jerusalem website once a week.
2.  🏟️ **Identifies** home games at Teddy Stadium.
3.  📅 **Adds** events to a public Google Calendar.
4.  🔔 **Sends a reminder** the day before - no parking!

## 🚀 Installation

### Step 1: Fork the Repository

Click "Fork" at the top of this page to create your own copy.

### Step 2: Set up Google Calendar API

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  Enable the **Google Calendar API**.
4.  Create a **Service Account** (not OAuth! This is simpler for GitHub Actions).
5.  Download the JSON credentials file.
6.  Save the content as `GOOGLE_CREDENTIALS` in your repository's secrets.

#### How to create a Service Account:

```
IAM & Admin → Service Accounts → Create
├── Name: beitar-calendar-sync
├── Role: Editor (or Calendar API → Calendar Editor)
└── Create Key → JSON → Download
```

#### How to set up GitHub Secrets:

Go to `Settings → Secrets and variables → Actions → New repository secret`:

| Secret Name        | Description                          |
| ------------------ | ------------------------------------ |
| `GOOGLE_CREDENTIALS` | The content of the downloaded JSON file |
| `CALENDAR_ID`      | The ID of your public calendar       |

### Step 3: Create a Public Calendar (Optional but Recommended!)

If you want anyone with the link to be able to subscribe to the calendar:

1.  Open [Google Calendar](https://calendar.google.com).
2.  Click the **+** next to "Other calendars" → **Create new calendar**.
3.  Name: `Beitar's Home Games at Teddy - No Parking!`
4.  Click **Create calendar**.
5.  Find the calendar in the sidebar → three dots → **Settings and sharing**.
6.  Scroll to **Access permissions**.
7.  Check **Make available to public** → **See all event details**.
8.  Scroll down to **Integrate calendar** and copy the **Calendar ID**.

### Step 4: Share the Calendar with the Service Account

1.  In the same settings screen, scroll to **Share with specific people**.
2.  Add the Service Account's email address (it looks like `beitar-calendar@PROJECT.iam.gserviceaccount.com`).
3.  Give it the **Make changes to events** permission.

### Step 5: Verify Everything Works

1.  Go to `Actions → Sync Beitar Games to Calendar`.
2.  Click **Run workflow**.
3.  Check the logs.

### 🔗 Share the Calendar with Others

After making the calendar public, you can share it with others:

| Type | URL |
|---|---|
| **View in Browser** | `https://calendar.google.com/calendar/embed?src=15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com` |
| **iCal (Apple/Outlook)** | `https://calendar.google.com/calendar/ical/15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com/public/basic.ics` |
| **Click to Subscribe** | `https://calendar.google.com/calendar/render?cid=15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com` |

## ⚙️ Configuration

### Changing the Run Frequency

Edit `.github/workflows/sync-calendar.yml`:

```yaml
on:
  schedule:
    - cron: '0 6 * * 0' # Every Sunday at 9:00 AM (Israel time)
    # - cron: '0 6 1 * *'  # Once a month
```

### Changing Reminders

Edit `src/calendar_sync.py`:

```python
'reminders': {
    'overrides': [
        {'method': 'popup', 'minutes': 24 * 60},   # One day before
    ],
},
```

## 📁 Project Structure

```
beitar-calendar-sync/
├── .github/
│   └── workflows/
│       └── sync-calendar.yml    # GitHub Action
├── src/
│   ├── scraper.py               # Scraper for the Beitar website
│   ├── calendar_sync.py         # Syncs to Google Calendar
│   └── main.py                  # Entry point
├── requirements.txt             # Dependencies
└── README.md                    # You are here!
```

## 🧪 Local Testing

```bash
# Installation
pip install -r requirements.txt

# Dry run (no actual changes)
export DRY_RUN=true
export GOOGLE_CREDENTIALS='{"type": "service_account", ...}'
python src/main.py

# Real run
export DRY_RUN=false
python src/main.py
```

## 🐛 Troubleshooting

### "Calendar not found"

-   Make sure you shared the calendar with the Service Account.
-   Verify that the `CALENDAR_ID` is correct.

### "Invalid credentials"

-   Make sure the JSON in `GOOGLE_CREDENTIALS` is valid.
-   Make sure the Service Account is enabled.

### Games are not being scraped

-   The website's structure might have changed - check `src/scraper.py`.
-   Run `python src/scraper.py` to test locally.

## 📄 License

MIT License - do whatever you want with it! 🟡⚫

---

<p align="center">
  <strong>Yalla Beitar! 🟡⚫</strong>
</p>

<details>
<summary>עברית</summary>

# 🟡⚫ Beitar Calendar Sync

> אוטומציה שמסנכרנת משחקי בית של בית"ר ירושלים בטדי ליומן גוגל - כדי שלא תשכחו להזיז את הרכב!

[![Sync Calendar](https://github.com/YOUR_USERNAME/beitar-calendar-sync/actions/workflows/sync-calendar.yml/badge.svg)](https://github.com/YOUR_USERNAME/beitar-calendar-sync/actions/workflows/sync-calendar.yml)

## 📖 מה זה עושה?

1. 🕷️ **סורק** את אתר בית"ר ירושלים אחת לשבוע
2. 🏟️ **מזהה** משחקי בית באצטדיון טדי
3. 📅 **מוסיף** אירועים ליומן ציבורי בגוגל
4. 🔔 **תזכורת** יום לפני - אין חניה!

## 🚀 התקנה

### שלב 1: Fork את הריפו

לחץ על "Fork" למעלה וצור עותק משלך.

### שלב 2: הגדר Google Calendar API

1. לך ל-[Google Cloud Console](https://console.cloud.google.com/)
2. צור פרויקט חדש
3. הפעל את **Google Calendar API**
4. צור **Service Account** (לא OAuth! זה יותר פשוט ל-GitHub Actions)
5. הורד את קובץ ה-JSON של ה-credentials
6. שמור את התוכן כ-`GOOGLE_CREDENTIALS` ב-Repository Secrets

#### איך ליצור Service Account:

```
IAM & Admin → Service Accounts → Create
├── Name: beitar-calendar-sync
├── Role: Editor (או Calendar API → Calendar Editor)
└── Create Key → JSON → Download
```

#### הגדרת Secrets ב-GitHub:

לך ל-`Settings → Secrets and variables → Actions → New repository secret`:

| Secret Name | תיאור |
|-------------|-------|
| `GOOGLE_CREDENTIALS` | תוכן קובץ ה-JSON שהורדת |
| `CALENDAR_ID` | ID של היומן הציבורי |

### 🔗 שיתוף היומן עם אחרים

אחרי שהיומן ציבורי, תוכל לשתף:

| סוג | URL |
|-----|-----|
| **צפייה בדפדפן** | `https://calendar.google.com/calendar/embed?src=15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com` |
| **iCal (Apple/Outlook)** | `https://calendar.google.com/calendar/ical/15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com/public/basic.ics` |
| **הרשמה בקליק** | `https://calendar.google.com/calendar/render?cid=15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com` |

### שלב 3: צור יומן ציבורי (אופציונלי אבל מומלץ!)

אם אתה רוצה שכל מי שיש לו הלינק יוכל להירשם ליומן:

1. פתח את [Google Calendar](https://calendar.google.com)
2. לחץ על **+** ליד "Other calendars" → **Create new calendar**
3. שם: `משחקי בית"ר בטדי - אין חניה!`
4. לחץ **Create calendar**
5. מצא את היומן בסרגל הצדדי → שלוש נקודות → **Settings and sharing**
6. גלול ל-**Access permissions**
7. סמן **Make available to public** → **See all event details**
8. גלול למטה ל-**Integrate calendar** והעתק את ה-**Calendar ID**

### שלב 4: שתף את היומן עם ה-Service Account

1. באותו מסך ההגדרות, גלול ל-**Share with specific people**
2. הוסף את האימייל של ה-Service Account (נראה כמו `beitar-calendar@PROJECT.iam.gserviceaccount.com`)
3. תן הרשאת **Make changes to events**

### שלב 5: בדוק שהכל עובד

1. לך ל-`Actions → Sync Beitar Games to Calendar`
2. לחץ **Run workflow**
3. בדוק את הלוגים

## ⚙️ הגדרות

### שינוי תדירות הריצה

ערוך `.github/workflows/sync-calendar.yml`:

```yaml
on:
  schedule:
    - cron: '0 6 * * 0'  # כל יום ראשון ב-9:00 (ישראל)
    # - cron: '0 6 1 * *'  # פעם בחודש
```

### שינוי תזכורות

ערוך `src/calendar_sync.py`:

```python
'reminders': {
    'overrides': [
        {'method': 'popup', 'minutes': 24 * 60},   # יום לפני
    ],
},
```

## 📁 מבנה הפרויקט

```
beitar-calendar-sync/
├── .github/
│   └── workflows/
│       └── sync-calendar.yml    # GitHub Action
├── src/
│   ├── scraper.py               # סקרייפר לאתר בית"ר
│   ├── calendar_sync.py         # סינכרון ל-Google Calendar
│   └── main.py                  # נקודת כניסה
├── requirements.txt             # תלויות
└── README.md                    # אתה כאן!
```

## 🧪 בדיקה מקומית

```bash
# התקנה
pip install -r requirements.txt

# ריצה יבשה (ללא שינויים אמיתיים)
export DRY_RUN=true
export GOOGLE_CREDENTIALS='{"type": "service_account", ...}'
python src/main.py

# ריצה אמיתית
export DRY_RUN=false
python src/main.py
```

## 🐛 פתרון בעיות

### "Calendar not found"

- ודא ששיתפת את ה-Service Account עם היומן
- בדוק שה-`CALENDAR_ID` נכון

### "Invalid credentials"

- ודא שה-JSON ב-`GOOGLE_CREDENTIALS` תקין
- ודא שה-Service Account מופעל

### המשחקים לא נשלפים

- האתר עשוי להשתנות - בדוק את `src/scraper.py`
- הרץ `python src/scraper.py` לבדיקה מקומית

## 📄 רישיון

MIT License - תעשו מה שבא לכם! 🟡⚫

---

<p align="center">
  <strong>יהיה בית"ר! 🟡⚫</strong>
</p>

</details>
