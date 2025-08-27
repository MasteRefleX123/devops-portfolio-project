### סיכום התקדמות CI/CD (PUSH/PULL)

- **מצב נוכחי**
  - בדיקות עברו (31/31, ~77%).
  - Build+Push עובדים (v34).
  - Deploy טרם הושלם, Jenkinsfile עודכן למניעת prompt ולהעדפת KUBECONFIG_BASE64.
  - הוסף .dockerignore לצמצום context.

- **בעיות פתוחות**
  - kubeconfig ב-Jenkins דורש רענון/אימות non-interactive.

- **תוכנית מיידית**
  1) לרענן kubeconfig credential ב-Jenkins.
  2) להריץ Deploy ולאמת rollout.
  3) להוסיף smoke test ל-/health.
  4) להפעיל DOCKER_BUILDKIT ולהקל Setup.

- **הערכת זמן**: ~20-30 דק׳ לייצוב Deploy ועוד ~20-30 דק׳ ל-smoke+אופטימיזציות.

