const express = require("express");
const Database = require("better-sqlite3");
const path = require("path");
const cors = require("cors");


const app = express();
const PORT = process.env.PORT || 3000;
const DUMMY_PASSWORD = "CyberLab2026!";

const db = new Database(path.join(__dirname, "simulation.db"));

db.exec(`
  CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_identifier TEXT NOT NULL,
    entered_value TEXT NOT NULL DEFAULT '',
    submitted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
  )
`);

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));
app.use(cors({
    origin: ["http://127.0.0.1:5000", "http://localhost:5000"]
}));

app.post("/api/submit", (req, res) => {
  const { account, password } = req.body;

  if (typeof account !== "string" || !account.trim()) {
    return res.status(400).json({ success: false, message: "Account identifier is required." });
  }

  const enteredValue = typeof password === "string" ? password.trim() : "";

  const insert = db.prepare(`
    INSERT INTO submissions (account_identifier, entered_value)
    VALUES (?, ?)
  `);

  insert.run(account.trim(), enteredValue);

  res.json({ success: true, message: "Simulation submission recorded." });
});

app.get("/api/submissions", (req, res) => {
  const rows = db.prepare(`
    SELECT id, account_identifier, entered_value, submitted_at
    FROM submissions
    ORDER BY id DESC
  `).all();

  res.json(rows.map(row => ({
    id: row.id,
    account_identifier: row.account_identifier,
    entered_value: row.entered_value,
    submitted_at: row.submitted_at
  })));
});
app.get("/admin", (req, res) => {
  res.sendFile(path.join(__dirname, "static", "admin.html"));
});

app.listen(PORT, () => {
  console.log(`Simulation running at http://localhost:${PORT}`);
  console.log(`Admin dashboard: http://localhost:${PORT}/admin`);
});
