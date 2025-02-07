### **Collaboration Workflow for Git & GitHub**

This is an example collaboration for git & github. Can be used as reference.

---

## **1️⃣ Set Up GitHub Repository**

1.  **Clone the repository (each person runs this on their machine):**

```
git clone https://github.com/HoJoeNiel/Classtrack-Backend.git
cd Classtrack-Backend
```

---

## **2️⃣ Use a Branching Strategy**

Use **feature branches** to avoid breaking the `main` branch.

### ✅ **Branch Naming Convention**

- `main` → Stable, production-ready branch
- `dev` → Main working branch for development

  **_Below are examples only_**

  **_Yours will depend on the name of the feature you're working on_**

- Feature branches:
- `feature-auth` → Authentication system
- `feature-users` → User-related endpoints
- `feature-db` → Database setup

Each developer works **only on their feature branch**.

### 🔀 **Creating a Feature Branch**

`git checkout -b feature-users  # Create and switch to new branch`

---

## **3️⃣ Making Changes**

1.  **Write code for your assigned feature.**
2.  **Add and commit changes:**

```
  git add .
  git commit -m "Added user authentication endpoint"
```

3.  **Push the branch to GitHub:**

```
   git push origin feature-users`
```

---

## **4️⃣ Merge Changes Using Pull Requests (PRs)**

1.  **Go to GitHub → Pull Requests → New PR**
2.  **Select:**
    - **Base branch:** `dev`
    - **Compare branch:** `feature-users`
3.  **Create PR & Request Review** from teammates.
4.  Once approved, **merge into `dev`**.

---

## **5️⃣ Keep Your Branch Updated**

Before working on your branch, **sync with the latest `dev` changes** to avoid conflicts.

### 🔄 **Pull Latest Changes**

```
git checkout dev
git pull origin dev  # Get latest code
git checkout feature-users
git merge dev  # Merge dev into your branch
```

Resolve conflicts if needed, then commit and push.
