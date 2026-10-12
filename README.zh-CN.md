<div align="center">

# Loggia website

Loggia 官网（useloggia.com）的源码：九种语言的静态网站，部署在 Cloudflare Workers 上。

[![CI](https://github.com/ydongy/loggia-website/actions/workflows/ci.yml/badge.svg)](https://github.com/ydongy/loggia-website/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/website-useloggia.com-informational.svg)](https://useloggia.com)

[English](README.md) · **简体中文**

</div>

<p align="center"><img src="public/og.png" alt="Loggia website" width="640"></p>

## 功能特性

- 九种语言：英文、简体中文、繁体中文、日文、韩文、法文、德文、西班牙文、葡萄牙文，以英文为基准。
- 静态生成：`i18n/*.json` 与 `changelog.json` 经 `scripts/build.py` 生成 `public/`；只用 Python 标准库，无框架，无需安装依赖。
- 每个页面只有一个地址，没有重定向和别名；首次访问会按浏览器语言跳转到受支持的语言。
- 以 Cloudflare Workers 静态资源方式部署（`wrangler.jsonc`），Content-Security-Policy 写在 `public/_headers`。
- 无 Cookie，除 Cloudflare Web Analytics 外无第三方代码；CI 中检查 i18n 一致性、链接与锚点、CSP 和法律事实数据。

## 环境要求

- Python 3（仅标准库）。
- 可选：Node.js，用于 `npx wrangler dev` 和部署。

## 快速开始

```bash
git clone https://github.com/ydongy/loggia-website.git
cd loggia-website
python3 scripts/sitekit/preview.py      # 本地预览 public/，并打印访问地址
```

`preview.py` 能像线上一样处理 `/zh/privacy` 这类无扩展名路径，`python3 -m http.server` 不行。也可以用 `npx wrangler dev`。

## 使用方法

### 页面

| 页面 | 地址 | 文案来源 |
|---|---|---|
| 首页（含 `#download`、`#pricing`） | `/` | `i18n/<code>.json` 中的 `home` |
| FAQ | `/faq` | `faq` |
| 更新日志 | `/changelog` | `changelog.json` |
| 隐私政策 | `/privacy` | `privacy` |
| 服务条款 | `/terms` | `terms` |
| 退款政策 | `/refund` | `refund` |
| 支持 | `/support` | `support` |
| 404 | `/404` | 自动生成 |

其他语言加路径前缀（`/zh/faq`、`/zh-hant/terms` 等）。详见 [docs/content.md](docs/content.md)。

### 语言

`en`、`zh`、`zh-hant`、`ja`、`ko`、`fr`、`de`、`es`、`pt`。新增语言（请先开 Issue）：在 `i18n/languages.json` 中登记，把 `i18n/en.json` 翻译为 `i18n/<code>.json`，结构和 JSON 格式保持一致，以及五组截图 `public/img/app-<code>-<scene>-{light,dark}.webp`（见 [docs/adr/0006-screenshot-carousel.md](docs/adr/0006-screenshot-carousel.md)），然后重新构建并运行下面的检查。

### 内容来源

- 事实数据（价格、套餐限制、退款期限等）来自产品自己的事实清单；[docs/content.md](docs/content.md) 中的 Facts 表与之对应，`scripts/check_facts.py` 会对照该表检查每种语言。
- `changelog.json` 由 Loggia 发布流程自动更新：每次发版会向本仓库提交一个 Pull Request。请勿手工编辑，并保持其路径和格式（见 [docs/contracts.md](docs/contracts.md)）。
- 服务条款依据应用的许可文本翻译；隐私政策和退款政策在本仓库撰写。

### 与应用的约定

应用会链接到 `/privacy`、`/terms`、`/refund`、`/changelog` 和 `/#pricing`，这些地址保持稳定。下载按钮读取 `https://dl.useloggia.com/latest.json`（版本号与校验和，由应用的发布流程写入）。如果该地址变化，需同步修改 `public/_headers` 中的 `connect-src`。

## 开发

修改 `i18n/*.json`、`public/style.css` 或 `scripts/build.py`（`changelog.json` 由发布流程更新）；不要直接改生成的 HTML 和 `public/lang.js`。然后按顺序运行（与 [CI](.github/workflows/ci.yml) 一致）：

```bash
python3 scripts/sitekit/check_i18n.py   # 各语言与英文结构、标签、链接、占位符一致
python3 scripts/build.py                # 重新生成 public/
git diff --exit-code -- public/         # 已提交的产物与源文件一致
python3 scripts/sitekit/check_site.py   # 页面、链接、锚点、Content-Security-Policy
python3 scripts/check_facts.py          # docs/content.md 的 Facts 表与各语言一致
```

生成的 `public/` 要和对应的源文件改动一起提交，否则 CI 会报 "public/ is stale"。
- 分享图 `public/og.png`（1200x630）由 `scripts/export-og.sh` 用无头 Chrome 从 `design/og.html` 渲染；图标或标语变化时需重新生成。

```
.
├── i18n/                    # 各语言文案（en.json 为基准）、languages.json
├── changelog.json           # 版本历史，由发布流程写入
├── design/                  # 分享图源文件（og.html）
├── scripts/
│   ├── build.py             # 生成器与站点设置
│   ├── check_facts.py       # 法律事实检查
│   └── sitekit/             # 内置的页面生成、检查与预览工具
├── public/                  # 生成的站点，需提交
├── docs/                    # 内容、设计、约定、ADR
└── wrangler.jsonc           # Cloudflare Workers 静态资源配置
```

`scripts/sitekit/` 是 ydongy 的 sitekit 的内置副本，请在上游修改，不要改这里（[ADR](docs/adr/0005-vendored-sitekit.md)）。更多：[docs/design.md](docs/design.md)、[docs/contracts.md](docs/contracts.md)、[AGENTS.md](AGENTS.md)。

### 部署

由 Cloudflare Workers Builds 从 `main` 自动部署：项目 `loggia`，构建命令留空，部署命令 `npx wrangler deploy`，按 `wrangler.jsonc` 发布 `public/`。部署时不会构建，所以 `public/` **必须提交**。自定义域名在 Cloudflare 控制台中绑定，不在配置文件里；`workers_dev` 和 `preview_urls` 有意关闭。

运维细节（域名绑定、构建检查、响应头、邮件转发）见 [docs/deployment.md](docs/deployment.md)。

## 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。较大的改动请先开 Issue。提交信息和 PR 标题使用 [Conventional Commits](https://www.conventionalcommits.org/)。

## 安全

请通过 GitHub Security 私下报告漏洞：[Report a vulnerability](https://github.com/ydongy/loggia-website/security/advisories/new)，不要公开提 Issue。

## 许可证

本仓库的源代码以 [MIT 许可证](LICENSE) 发布。

Loggia 的名称、Logo、图标以及网站文案（文字与译文）版权归 ydongy 所有（copyright (c) 2026），**不在** MIT 授权范围内。Loggia 是闭源产品（仅本网站开源）；名称和图标不得用于暗示认可，也不得用于命名衍生作品。
