# 🟡⚫ Beitar Jerusalem Calendar Sync

> An automation that syncs Beitar Jerusalem's home games at Teddy Stadium to a Google Calendar - so you won't forget to move your car!

[![Sync Calendar](https://github.com/YOUR_USERNAME/beitar-calendar-sync/actions/workflows/sync-calendar.yml/badge.svg)](https://github.com/YOUR_USERNAME/beitar-calendar-sync/actions/workflows/sync-calendar.yml)

## 🔗 Subscribe to the Calendar

Easily add Beitar Jerusalem's home games to your calendar:

| Type | URL |
|---|---|
| **View in Browser** | `https://calendar.google.com/calendar/embed?src=15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com` |
| **iCal (Apple/Outlook)** | `https://calendar.google.com/calendar/ical/15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com/public/basic.ics` |
| **Click to Subscribe** | `https://calendar.google.com/calendar/render?cid=15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com` |

## 📖 What does it do?

This project automatically:
1.  🕷️ **Scrapes** the Beitar Jerusalem website once a week.
2.  🏟️ **Identifies** home games at Teddy Stadium.
3.  📅 **Adds** events to the public Google Calendar linked above.
4.  🔔 **Sends a reminder** the day before - no parking!

## 🚀 Setup for Self-Hosting (Advanced)

If you wish to run this automation yourself, follow these steps:

### 1. Fork the Repository

Click "Fork" at the top of this page to create your own copy.

### 2. Configure Google Calendar API

You'll need a Google Cloud Project with the Calendar API enabled and a Service Account key.
Store the JSON content of your Service Account key as a GitHub Secret named `GOOGLE_CREDENTIALS`.
Also, create a public Google Calendar and store its ID as a GitHub Secret named `CALENDAR_ID`.

For detailed instructions on setting up Google Calendar API and Service Accounts, refer to the [Google Cloud documentation](https://cloud.google.com/docs/authentication/getting-started).

### 3. Verify Setup

After configuration, you can manually trigger the workflow:
1.  Go to `Actions → Sync Beitar Games to Calendar`.
2.  Click **Run workflow**.
3.  Check the logs for successful sync.

## ⚙️ Configuration Options

### Changing the Run Frequency

Edit `.github/workflows/sync-calendar.yml` to adjust the `cron` schedule.

### Changing Reminders

Edit `src/calendar_sync.py` to modify event reminders.

## 🐛 Troubleshooting

-   **"Calendar not found"**: Ensure `CALENDAR_ID` is correct and the Service Account has access.
-   **"Invalid credentials"**: Verify `GOOGLE_CREDENTIALS` JSON is valid and the Service Account is enabled.
-   **Games not scraped**: The website structure might have changed. Check `src/scraper.py`.

## 📄 License

MIT License - do whatever you want with it! 🟡⚫

---

<p align="center">
  <strong>Yalla Beitar! 🟡⚫</strong>
</p>

<details>
<summary>עברית</summary>

# 🟡⚫ סנכרון לוח שנה בית"ר

> אוטומציה שמסנכרנת משחקי בית של בית"ר ירושלים בטדי ליומן גוגל - כדי שלא תשכחו להזיז את הרכב!

[![Sync Calendar](https://github.com/YOUR_USERNAME/beitar-calendar-sync/actions/workflows/sync-calendar.yml/badge.svg)](https://github.com/YOUR_USERNAME/beitar-calendar-sync/actions/workflows/sync-calendar.yml)

## 🔗 הירשם ללוח השנה

הוסף בקלות את משחקי הבית של בית"ר ירושלים ליומן שלך:

| סוג | URL |
|---|---|
| **צפייה בדפדפן** | `https://calendar.google.com/calendar/embed?src=15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com` |
| **iCal (Apple/Outlook)** | `https://calendar.google.com/calendar/ical/15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com/public/basic.ics` |
| **הרשמה בקליק** | `https://calendar.google.com/calendar/render?cid=15136f57a49bb2811aab2eadc7624fbf11953b21ca9dd55257066a8249557a3@group.calendar.google.com` |

## 📖 מה זה עושה?

פרויקט זה מבצע באופן אוטומטי:
1.  🕷️ **סורק** את אתר בית"ר ירושלים אחת לשבוע.
2.  🏟️ **מזהה** משחקי בית באצטדיון טדי.
3.  📅 **מוסיף** אירועים ליומן הגוגל הציבורי המקושר לעיל.
4.  🔔 **שולח תזכורת** יום לפני - אין חניה!

## 🚀 הגדרה להרצה עצמית (מתקדם)

אם ברצונך להריץ אוטומציה זו בעצמך, בצע את השלבים הבאים:

### 1. Fork את הריפו

לחץ על "Fork" למעלה וצור עותק משלך.

### 2. הגדר Google Calendar API

תזדקק לפרויקט ב-Google Cloud עם Calendar API מופעל ומפתח Service Account.
שמור את תוכן ה-JSON של מפתח ה-Service Account שלך כ-GitHub Secret בשם `GOOGLE_CREDENTIALS`.
כמו כן, צור יומן גוגל ציבורי ושמור את ה-ID שלו כ-GitHub Secret בשם `CALENDAR_ID`.

להוראות מפורטות על הגדרת Google Calendar API ו-Service Accounts, עיין ב-[תיעוד של Google Cloud](https://cloud.google.com/docs/authentication/getting-started).

### 3. ודא שהכל עובד

לאחר ההגדרה, תוכל להפעיל את ה-workflow באופן ידני:
1.  לך ל-`Actions → Sync Beitar Games to Calendar`.
2.  לחץ **Run workflow**.
3.  בדוק את הלוגים לוודא סנכרון מוצלח.

## ⚙️ אפשרויות תצורה

### שינוי תדירות הריצה

ערוך את `.github/workflows/sync-calendar.yml` כדי להתאים את לוח הזמנים של ה-`cron`.

### שינוי תזכורות

ערוך את `src/calendar_sync.py` כדי לשנות את תזכורות האירועים.

## 🐛 פתרון בעיות

-   **"Calendar not found"**: ודא שה-`CALENDAR_ID` נכון ול-Service Account יש גישה.
-   **"Invalid credentials"**: ודא שה-JSON ב-`GOOGLE_CREDENTIALS` תקין ושה-Service Account מופעל.
-   **המשחקים לא נשלפים**: ייתכן שמבנה האתר השתנה. בדוק את `src/scraper.py`.

## 📄 רישיון

MIT License - תעשו מה שבא לכם! 🟡⚫

---

<p align="center">
  <strong>יהיה בית"ר! 🟡⚫</strong>
</p>

</details>