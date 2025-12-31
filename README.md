<p align="center">
  <img src="https://iili.io/KhN0ztj.png" alt="Logo" width="400"/>
</p>


<p align="center">
  A powerful, self-hosted <b>Telegram & Google Drive Stremio Media Server</b> built with <b>FastAPI</b>, <b>MongoDB</b>, and <b>PyroFork</b> — seamlessly integrated with <b>Stremio</b> for automated media streaming and discovery.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/UV%20Package%20Manager-2B7A77?logo=uv&logoColor=white" alt="UV Package Manager" />
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/PyroFork-EE3A3A?logo=python&logoColor=white" alt="PyroFork" />
  <img src="https://img.shields.io/badge/Stremio-8D3DAF?logo=stremio&logoColor=white" alt="Stremio" />
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Google%20Drive-4285F4?logo=googledrive&logoColor=white" alt="Google Drive" />
</p>

---

## 🧭 Quick Navigation

- [🚀 Introduction](#-introduction)
  - [✨ Key Features](#-key-features)
- [⚙️ How It Works](#️-how-it-works)
  - [Overview](#overview)
  - [Upload Guidelines](#upload-guidelines)
  - [Quality Replacement](#-quality-replacement-logic)
  - [Updating CAMRip](#-updating-camrip-or-low-quality-files)
  - [Behind The Scenes](#behind-the-scenes)
- [🤖 Bot Commands](#-bot-commands)
  - [Command List](#command-list)
  - [`/set` Command Usage](#set-command-usage)
- [🔧 Configuration Guide](#-configuration-guide)
  - [🧩 Startup Config](#-startup-config)
  - [🗄️ Storage](#️-storage)
  - [🎬 API](#-api)
  - [🌐 Server](#-server)
  - [🔄 Update Settings](#-update-settings)
  - [🔐 Admin Panel](#-admin-panel)
  - [🧰 Additional CDN Bots (Multi-Token System)](#-additional-cdn-bots-multi-token-system)
- [🚀 Deployment Guide](#-deployment-guide)
  - [✅ Recommended Prerequisites](#-recommended-prerequisites)
  - [🐙 Heroku Guide](#-heroku-guide)
  - [🐳 VPS Guide (Recommended)](#-vps-guide)
- [📺 Setting up Stremio](#-setting-up-stremio)
  - [🌐 Add the Addon](#-step-3-add-the-addon)
  - [⚙️ Optional: Remove Cinemeta](#️-optional-remove-cinemeta)
- [🏅 Contributor](#-contributor)


# 🚀 Introduction

This project is a **next-generation Media Server** that allows you to **stream your Telegram files and Google Drive links directly through Stremio**, without any third-party dependencies or file expiration issues. It’s designed for **speed, scalability, and reliability**, making it ideal for both personal and community-based media hosting.


## ✨ Key Features

- ⚙️ **Multiple MongoDB Support** - 📡 **Multiple Channel Support** - 📂 **Google Drive Integration**
- ⚡ **Fast Streaming Experience**
- 🔑 **Multi Token Load Balancer** - 🎬 **IMDB and TMDB Metadata Integration** - ♾️ **No File Expiration** - 🧠 **Admin Panel Support** ## ⚙️ How It Works

This project acts as a **bridge between Telegram/GDrive storage and Stremio streaming**, connecting **Telegram**, **Google Drive API**, **FastAPI**, and **Stremio** to enable seamless movie and TV show streaming.

### Overview

When you **forward Telegram files** or **send Google Drive links** to your **AUTH CHANNEL**, the bot automatically:

1.  🗃️ **Stores** the reference (message_id or file_id) in the database.
2.  🧠 **Processes** file captions or filenames to extract key metadata (title, year, quality, etc.).
3.  🌐 **Generates a streaming URL** routed by **FastAPI**.
4.  🎞️ **Provides Stremio Addon APIs**:
    -   `/catalog` → Lists available media
    -   `/meta` → Shows detailed information for each item
    -   `/stream` → Streams the file directly

### Upload Guidelines

To ensure proper metadata extraction and seamless integration with **Stremio**, all uploaded media files **must include specific details** in their captions (Telegram) or filenames (Google Drive).

#### 🎥 For Movies

**Example Caption / Filename:**
