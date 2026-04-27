# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-04-27
### Fixed
- 修復 GitHub Actions 環境下 `data/plots` 目錄不存在導致繪圖失敗的問題。
- 修復 Linux Headless 環境下 Matplotlib 的渲染問題 (切換至 Agg 後端)。
- 修正 `.gitignore` 阻擋自動化報表上傳的問題 (改用 `add -f` 策略)。

### Added
- 導入 GitHub Actions 自動化工作流 (每週一至五 14:00 自動執行)。
- 建立 `daily-results` 獨立分支，分離程式碼與數據結果。

## [1.0.0] - 2026-04-26
### Added
- 核心 DMI/ADX 技術指標計算邏輯。
- 物件導向重構 (OOP) 與單元測試框架。
- 導入中央日誌系統 (Logging) 取代 print。
- 增加 MIT License 授權條款。