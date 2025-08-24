## ערוץ תקשורת לסוכן 2 – נושא: PAGER

מטרה: לאבחן ולפתור בעיית pager (למשל less) שמפעיל גלילה/חסימה בכלי CLI.

### מה צריך לעשות
1) מלא/י תשובות קצרות ל"שאלות אבחון" בקובץ `RESPONSES.md`.
2) הרץ/י את סקריפט הדיאגנוסטיקה:
```bash
bash .workspace/agents/pager/run_diagnostics.sh | tee .workspace/agents/pager/reports/$(date +%Y%m%d-%H%M%S).txt
```
3) אם עדיין נתקע/נפתח pager, השתמש/י זמנית בעקיפה המהירה למטה עד שנקבע פתרון קבוע.

### שאלות אבחון (נא להשיב ב־RESPONSES.md)
- מה התסמין המדויק? אילו פקודות נפתחות ב־pager/נתקעות?
- היכן זה קורה? טרמינל אינטראקטיבי/CI (Jenkins)/שניהם?
- באיזה shell/OS/סביבה (bash/zsh, Linux/WSL/Container)?
- ערכי משתני הסביבה: `PAGER`, `GIT_PAGER`, `MANPAGER`, `AWS_PAGER`, `LESS`.
- `git config core.pager` (global/system/local) אם קיים.
- האם יש alias/כלי pager חלופי (למשל delta/bat/most/moar)?
- האם `git --no-pager ...` או `aws --no-cli-pager ...` פותרים נקודתית?
- דוגמת פקודה מינימלית שממחישה את הבעיה.

### עקיפה מהירה (זמנית לסשן הנוכחי)
```bash
export PAGER=cat
export GIT_PAGER=cat
export MANPAGER=cat
export AWS_PAGER=""
```

לאחר שנאסוף נתונים, ננטרל את ה־pager קבוע בקונפיג הנכון, לפי הממצאים.

מיקום דוחות: `.workspace/agents/pager/reports/`
