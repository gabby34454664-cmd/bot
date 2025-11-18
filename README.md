<p align="center">
  <img src="https://media.discordapp.net/attachments/1353062441398964414/1389659737221759096/thumbnail_Outlook-jghv2af0.png?ex=68656cfb&is=68641b7b&hm=2ac03622bd313bcf781e1404f95c157d7a35e2c4cb802eaa66bbd8b256a09d68&=&format=webp&quality=lossless&width=625&height=625" width="200" height="200" alt="ERLC Bot Logo"/>
</p>

<h1 align="center">ERLC Discord Bot</h1>
<p align="center"><b>Created by bob076161 (Discord)</b></p>

---

## ❓ Need Help?
Join the support server, verify, and open a **General Support Ticket**.  
Mention that **"the owner said to ask for him"** so support knows to escalate it.

> 🔗 **Discord Server**: [https://discord.gg/s9b5g666PV](https://discord.gg/s9b5g666PV)  
> 👑 **Bot Owner**: `bob076161` (on Discord)

---

## 🐞 Bug Reports
Please report bugs on GitHub:  
👉 [**Open a Bug Report**](https://github.com/bot6798098-075634/ERLC-Bot/issues/new?assignees=&labels=bug&template=bug_report.md&title=)

Include:
- Clear description of the issue  
- Steps to reproduce  
- Any screenshots or logs

---

## 💡 Feature Suggestions
Have an idea for a new feature? Suggest it here:  
👉 [**Submit a Suggestion**](https://github.com/bot6798098-075634/ERLC-Bot/issues/new?assignees=&labels=suggestion&template=feature_request.md&title=)

Include:
- What the feature does  
- Why it’s useful  
- Optional: how it might work

---

## ⚙️ Setup Instructions

### ✅ Recommended Setup (GitHub + Render)

1. Click **“Use this template”** on GitHub.
2. Create your own repository.
3. Delete the `.env` file.
4. Open `keep_alive.py` and update the following lines:

| Line # | What to Replace    | Replace With             |
|--------|--------------------|--------------------------|
| 33     | `server name`      | Your server name         |
| 34     | `image link`       | A valid image URL        |
| 162    | `image link`       | A valid image URL        |
| 162    | `server name`      | Your server name         |
| 164    | `server name`      | Your server name         |
| 190    | `server name`      | Your server name         |

---

### 🖥️ Hosting on Render

1. Go to [https://render.com](https://render.com) and **sign in**.
2. Go to your dashboard: [https://dashboard.render.com](https://dashboard.render.com)
3. Click **“Add New” → “Web Service”**.
4. Link your GitHub and select your repo.
5. Set the following:
   - **Start Command**: `python3 main.py`
   - **Instance Type**: Free
6. Add Environment Variables:
   - `DISCORD_TOKEN` → *(your bot token)*  
     👉 [**Watch How to Create & Get a Token**](https://www.youtube.com/watch?v=2cUg3Y50ytM)
   - `API_KEY` → *(your ERLC API key)*
7. Click **Deploy Web Service**.
8. Copy your URL (e.g., `https://erlc-bot-1wye.onrender.com`)

---

### ⏱️ Keep Alive with UptimeRobot

1. Visit [https://uptimerobot.com](https://uptimerobot.com)
2. Log in → go to [https://dashboard.uptimerobot.com](https://dashboard.uptimerobot.com)
3. Click **“New Monitor”**
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: ERLC Bot
   - **URL to Monitor**: your Render URL
4. Click **Create Monitor**

---

✅ Your ERLC Discord Bot is now online 24/7 and fully operational!
