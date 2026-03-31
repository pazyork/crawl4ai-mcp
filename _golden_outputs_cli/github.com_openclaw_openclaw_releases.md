# Releases · openclaw/openclaw

[Skip to content](https://github.com/openclaw/openclaw/releases#start-of-content)
You signed in with another tab or window. [Reload](https://github.com/openclaw/openclaw/releases) to refresh your session. You signed out in another tab or window. [Reload](https://github.com/openclaw/openclaw/releases) to refresh your session. You switched accounts on another tab or window. [Reload](https://github.com/openclaw/openclaw/releases) to refresh your session. Dismiss alert
{{ message }}
[ openclaw ](https://github.com/openclaw) / **[openclaw](https://github.com/openclaw/openclaw) ** Public
  * [ Sponsor  ](https://github.com/sponsors/openclaw)
  * [ Notifications ](https://github.com/login?return_to=%2Fopenclaw%2Fopenclaw) You must be signed in to change notification settings
  * [ Fork 65.4k ](https://github.com/login?return_to=%2Fopenclaw%2Fopenclaw)
  * [ Star  335k ](https://github.com/login?return_to=%2Fopenclaw%2Fopenclaw)

# Releases: openclaw/openclaw
Releases · openclaw/openclaw
## 2026.3.23
23 Mar 23:15
![@steipete](https://avatars.githubusercontent.com/u/58493?s=40&v=4) [steipete](https://github.com/steipete)
[ v2026.3.23  ](https://github.com/openclaw/openclaw/tree/v2026.3.23)
This tag was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
[ `ccfeecb`](https://github.com/openclaw/openclaw/commit/ccfeecb6887cd97937e33a71877ad512741e82b2)
This commit was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
Compare
#  Choose a tag to compare
## Sorry, something went wrong.
Filter
Loading
## Sorry, something went wrong.
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
## No results found
[View all tags](https://github.com/openclaw/openclaw/tags)
[2026.3.23](https://github.com/openclaw/openclaw/releases/tag/v2026.3.23) [Latest](https://github.com/openclaw/openclaw/releases/latest)
[Latest](https://github.com/openclaw/openclaw/releases/latest)
### Breaking
### Changes
  * ModelStudio/Qwen: add standard (pay-as-you-go) DashScope endpoints for China and global Qwen API keys alongside the existing Coding Plan endpoints, and relabel the provider group to `Qwen (Alibaba Cloud Model Studio)`. ([#43878](https://github.com/openclaw/openclaw/pull/43878))
  * UI/clarity: consolidate button primitives (`btn--icon`, `btn--ghost`, `btn--xs`), refine the Knot theme to a black-and-red palette with WCAG 2.1 AA contrast, add config icons for Diagnostics/CLI/Secrets/ACP/MCP sections, replace the roundness slider with discrete stops, and improve accessibility with aria-labels across usage filters. ([#53272](https://github.com/openclaw/openclaw/pull/53272)) Thanks [@BunsDev](https://github.com/BunsDev).
  * CSP/Control UI: compute SHA-256 hashes for inline `<script>` blocks in the served `index.html` and include them in the `script-src` CSP directive, keeping inline scripts blocked by default while allowing explicitly hashed bootstrap code. ([#53307](https://github.com/openclaw/openclaw/pull/53307)) Thanks [@BunsDev](https://github.com/BunsDev).

### Fixes
  * Plugins/bundled runtimes: ship bundled plugin runtime sidecars like WhatsApp `light-runtime-api.js`, Matrix `runtime-api.js`, and other plugin runtime entry files in the npm package again, so global installs stop failing on missing bundled plugin runtime surfaces.
  * CLI/channel auth: auto-select the single configured login-capable channel for `channels login`/`logout`, harden channel ids against prototype-chain and control-character abuse, and fall back cleanly to catalog-backed channel installs, so channel auth works again for single-channel setups and on-demand channel installs. ([#53254](https://github.com/openclaw/openclaw/pull/53254)) Thanks [@BunsDev](https://github.com/BunsDev).
  * Auth/OpenAI tokens: stop live gateway auth-profile writes from reverting freshly saved credentials back to stale in-memory values, and make `models auth paste-token` write to the resolved agent store, so Configure, Onboard, and token-paste flows stop snapping back to expired OpenAI tokens. Fixes [#53207](https://github.com/openclaw/openclaw/issues/53207). Related to [#45516](https://github.com/openclaw/openclaw/issues/45516).
  * Control UI/auth: preserve operator scopes through the device-auth bypass path, ignore cached under-scoped operator tokens, and show a clear `operator.read` fallback message when a connection really lacks read scope, so operator sessions stop failing or blanking on read-backed pages. ([#53110](https://github.com/openclaw/openclaw/pull/53110)) Thanks [@BunsDev](https://github.com/BunsDev).
  * Plugins/ClawHub: resolve plugin API compatibility against the active runtime version at install time, and add regression coverage for current `>=2026.3.22` ClawHub package checks so installs no longer fail behind the stale `1.2.0` constant. ([#53157](https://github.com/openclaw/openclaw/pull/53157)) Thanks [@futhgar](https://github.com/futhgar).
  * Plugins/uninstall: accept installed `clawhub:` specs and versionless ClawHub package names as uninstall targets, so `openclaw plugins uninstall clawhub:<package>` works again even when the recorded install was pinned to a version.
  * Browser/Chrome MCP: wait for existing-session browser tabs to become usable after attach instead of treating the initial Chrome MCP handshake as ready, which reduces user-profile timeouts and repeated consent churn on macOS Chrome attach flows. Fixes [#52930](https://github.com/openclaw/openclaw/issues/52930). Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Browser/CDP: reuse an already-running loopback browser after a short initial reachability miss instead of immediately falling back to relaunch detection, which fixes second-run browser start/open regressions on slower headless Linux setups. Fixes [#53004](https://github.com/openclaw/openclaw/issues/53004). Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Agents/web_search: use the active runtime `web_search` provider instead of stale/default selection, so agent turns keep hitting the provider you actually configured. Fixes [#53020](https://github.com/openclaw/openclaw/pull/53020). Thanks [@jzakirov](https://github.com/jzakirov).
  * Mistral/models: lower bundled Mistral max-token defaults to safe output budgets and teach `openclaw doctor --fix` to repair old persisted Mistral provider configs that still carry context-sized output limits, avoiding deterministic Mistral 422 rejects on fresh and existing setups. Fixes [#52599](https://github.com/openclaw/openclaw/issues/52599). Thanks [@vincentkoc](https://github.com/vincentkoc).
  * ClawHub/macOS auth: honor macOS auth config and XDG auth paths for saved ClawHub credentials, so `openclaw skills ...` and gateway skill browsing keep using the signed-in auth state instead of silently falling back to unauthenticated mode. Fixes [#53034](https://github.com/openclaw/openclaw/pull/53034).
  * ClawHub/macOS: read the local ClawHub login from the macOS Application Support path and still honor XDG config on macOS, so skill browsing uses the logged-in token on both default and XDG-style setups. Fixes [#52949](https://github.com/openclaw/openclaw/issues/52949). Thanks [@scoootscooob](https://github.com/scoootscooob).
  * ClawHub/skills: resolve the local ClawHub auth token for gateway skill browsing and switch browse-all requests to search so ClawControl stops falling into unauthenticated 429s and empty authenticated skill lists. Fixes [#52949](https://github.com/openclaw/openclaw/issues/52949). Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Config/warnings: suppress the confusing “newer OpenClaw” warning when a config written by a same-base correction release like `2026.3.23-2` is read by `2026.3.23`, while still warning for truly newer or incompatible versions.
  * CLI/cron: make `openclaw cron add|edit --at ... --tz <iana>` honor the requested local wall-clock time for offset-less one-shot datetimes, including DST boundaries, and keep `--tz` rejected for `--every`. ([#53224](https://github.com/openclaw/openclaw/pull/53224)) Thanks [@RolfHegr](https://github.com/RolfHegr).
  * Commands/auth: stop slash-command authorization from crashing or dropping valid allowlists when channel `allowFrom` resolution hits unresolved SecretRef-backed accounts, and fail closed only for the affected provider inference path. ([#52791](https://github.com/openclaw/openclaw/pull/52791)) Thanks [@Lukavyi](https://github.com/Lukavyi).
  * Agents/failover: classify generic `api_error` payloads as retryable only when they include transient failure signals, so MiniMax-style backend failures still trigger model fallback without misclassifying billing, auth, or format/context errors. ([#49611](https://github.com/openclaw/openclaw/pull/49611)) Thanks [@ayushozha](https://github.com/ayushozha).
  * LINE/runtime-api: pre-export overlapping runtime symbols before the `line-runtime` star export so jiti no longer throws `TypeError: Cannot redefine property` on startup. ([#53221](https://github.com/openclaw/openclaw/pull/53221)) Thanks [@Drickon](https://github.com/Drickon).
  * Telegram/threading: populate `currentThreadTs` in the threading tool-context fallback for Telegram DM topics so thread-aware tools still receive the active topic context when the main thread metadata is missing. ([#52217](https://github.com/openclaw/openclaw/issues/52217))
  * Diagnostics/cache trace: strip credential fields from cache-trace JSONL output while preserving non-sensitive diagnostic fields and image redaction metadata.
  * Docs/Feishu: replace `botName` with `name` in the channel config examples so the docs match the strict account schema for per-account display names. ([#52753](https://github.com/openclaw/openclaw/pull/52753)) Thanks [@haroldfabla2-hue](https://github.com/haroldfabla2-hue).
  * Doctor/plugins: make `openclaw doctor --fix` remove stale `plugins.allow` and `plugins.entries` refs left behind after plugin removal. Thanks [@sallyom](https://github.com/sallyom)
  * Agents/replay: canonicalize malformed assistant transcript content before session-history sanitization so legacy or corrupted assistant turns stop crashing Pi replay and subagent recovery paths.
  * ClawHub/skills: keep updating already-tracked legacy Unicode slugs after the ASCII-only slug hardening, so older installs do not get stuck behind `Invalid skill slug` errors during `openclaw skills update`. ([#53206](https://github.com/openclaw/openclaw/pull/53206)) Thanks [@drobison00](https://github.com/drobison00).
  * Infra/exec trust: preserve shell-multiplexer wrapper binaries for policy checks without breaking approved-command reconstruction, so BusyBox/ToyBox allowlist and audit flows bind to the real wrapper while execution plans stay coherent. ([#53134](https://github.com/openclaw/openclaw/pull/53134)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Plugins/message tool: make Discord `components` and Slack `blocks` optional again, and route Feishu `message(..., media=...)` sends through the outbound media path, so pin/unpin/react flows stop failing schema validation and Feishu file/image attachments actually send. Fixes [#52970](https://github.com/openclaw/openclaw/issues/52970) and [#52962](https://github.com/openclaw/openclaw/issues/52962). Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Gateway/model pricing: stop `openrouter/auto` pricing refresh from recursing indefinitely during bootstrap, so OpenRouter auto routes can populate cached pricing and `usage.cost` again. Fixes [#53035](https://github.com/openclaw/openclaw/issues/53035). Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Models/OpenAI Codex OAuth: bootstrap the env-configured HTTP/HTTPS proxy dispatcher on the stored-credential refresh path before token renewal runs, so expired Codex OAuth profiles can refresh successfully in proxy-required environments instead of locking users out after the first token expiry.
  * Models/OpenAI Codex OAuth and Plugins/MiniMax OAuth: ensure env-configured HTTP/HTTPS proxy dispatchers are initialized before OAuth preflight and token exchange requests so proxy-required environments can complete MiniMax and OpenAI Codex sign-in flows again. ([#52228](https://github.com/openclaw/openclaw/pull/52228); fixes [#51619](https://github.com/openclaw/openclaw/issues/51619), [#51569](https://github.com/openclaw/openclaw/issues/51569)) Thanks [@openperf](https://github.com/openperf).
  * Plugins/memory-lancedb: bootstrap LanceDB into plugin runtime state on first use when the bundled npm install does not already have it, so `plugins.slots.memory="memory-lancedb"` works again after global npm installs without moving LanceDB into OpenClaw core dependencies. Fixes [#26100](https://github.com/openclaw/openclaw/issues/26100).
  * Config/plugins: treat stale unknown `plugins.allow` ids as warnings instead of fatal config errors, so recovery commands like `plugins install`, `doctor --fix`, and `status` still run when a plugin is missing locally. Fixes [#52992](https://github.com/openclaw/openclaw/issues/52992). Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Doctor/WhatsApp: stop auto-enable from appending built-in channel ids like `whatsapp` to `plugins.allow`, so `openclaw doctor --fix` no longer writes schema-invalid plugin allowlist entries when repairing built-in channels. Fixes [#52931](https://github.com/openclaw/openclaw/issues/52931). Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Telegram/auto-reply: preserve same-chat inbound debounce order without stranding stale busy-session followups, and keep same-key overflow turns ordered when tracked debounce keys are saturated. ([#52998](https://github.com/openclaw/openclaw/pull/52998)) Thanks [@osolmaz](https://github.com/osolmaz).
  * Telegram/message tool: add `asDocument` as a user-facing alias for `forceDocument` on image and GIF sends, while preserving explicit `forceDocument` precedence when both flags are present. ([#52461](https://github.com/openclaw/openclaw/pull/52461)) Thanks [@bakhtiersizhaev](https://github.com/bakhtiersizhaev).
  * Discord/commands: return an explicit unauthorized reply for privileged native slash commands instead of falling through to Discord's misleading generic completion when auth gates reject the sender. Fixes [#53041](https://github.com/openclaw/openclaw/issues/53041). Thanks [@scoootscooob](https://github.com/scoootscooob).
  * Channels/catalog: let external channel catalogs override shipped fallback metadata and honor overridden npm specs during channel setup, so custom channel catalogs no longer fall back to bundled packages when a channel id matches. ([#52988](https://github.com/openclaw/openclaw/pull/52988))
  * Voice-call/Plivo: stabi...

[Read more](https://github.com/openclaw/openclaw/releases/tag/v2026.3.23)
### Contributors
  * [ ![@vincentkoc](https://avatars.githubusercontent.com/u/25068?s=64&v=4) ](https://github.com/vincentkoc)
  * [ ![@Lukavyi](https://avatars.githubusercontent.com/u/1013690?s=64&v=4) ](https://github.com/Lukavyi)
  * [ ![@osolmaz](https://avatars.githubusercontent.com/u/2453968?s=64&v=4) ](https://github.com/osolmaz)
  * [ ![@drobison00](https://avatars.githubusercontent.com/u/5256797?s=64&v=4) ](https://github.com/drobison00)
  * [ ![@ayushozha](https://avatars.githubusercontent.com/u/7945279?s=64&v=4) ](https://github.com/ayushozha)
  * [ ![@sallyom](https://avatars.githubusercontent.com/u/11166065?s=64&v=4) ](https://github.com/sallyom)
  * [ ![@jzakirov](https://avatars.githubusercontent.com/u/15848838?s=64&v=4) ](https://github.com/jzakirov)
  * [ ![@07akioni](https://avatars.githubusercontent.com/u/18677354?s=64&v=4) ](https://github.com/07akioni)
  * [ ![@Drickon](https://avatars.githubusercontent.com/u/41375613?s=64&v=4) ](https://github.com/Drickon)
  * [ ![@futhgar](https://avatars.githubusercontent.com/u/51002668?s=64&v=4) ](https://github.com/futhgar)
  * [ ![@BunsDev](https://avatars.githubusercontent.com/u/68980965?s=64&v=4) ](https://github.com/BunsDev)
  * [ ![@openperf](https://avatars.githubusercontent.com/u/80630709?s=64&v=4) ](https://github.com/openperf)
  * [ ![@RolfHegr](https://avatars.githubusercontent.com/u/92691215?s=64&v=4) ](https://github.com/RolfHegr)
  * [ ![@bakhtiersizhaev](https://avatars.githubusercontent.com/u/108124494?s=64&v=4) ](https://github.com/bakhtiersizhaev)
  * [ ![@scoootscooob](https://avatars.githubusercontent.com/u/167050519?s=64&v=4) ](https://github.com/scoootscooob)
  * [ ![@haroldfabla2-hue](https://avatars.githubusercontent.com/u/229189334?s=64&v=4) ](https://github.com/haroldfabla2-hue)

vincentkoc, Lukavyi, and 14 other contributors
Assets 5
Loading
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
👍 126 FergusClare, Hamjoon, Rubbishful, TycoonCoder, facadefish, kong62, dun4law, KBHKNKC, tienanh0903k, EndermanLV, and 116 more reacted with thumbs up emoji 😄 15 kong62, lin72h, artwalker, coolwolfqs, AceOf5pades, itshusky01, birdofprey, adoreking06, rabbitglauser, Jikerr, and 5 more reacted with laugh emoji 🎉 37 DeltaFROST141, BangyiZhang, Leon19960120, JayZhu03, carterzheng2010, robinbeier, FergusClare, ilne, rintaro-okahara, Rubbishful, and 27 more reacted with hooray emoji ❤️ 55 grubFX, AZLabsAI, TDaveCRC, thanhle98, trithanhalan, FLYCOM-E, kastner, orielhaim, NZF-JDWang, MyWay, and 45 more reacted with heart emoji 🚀 20 raistlin88, carterzheng2010, FergusClare, TycoonCoder, kong62, lin72h, tomrhudson, artwalker, coolwolfqs, mrverdant13, and 10 more reacted with rocket emoji 👀 17 zyzyzzyyy, FergusClare, TycoonCoder, kong62, helal-muneer, artwalker, JichenZhang, hufengxiao, pnoker, coolwolfqs, and 7 more reacted with eyes emoji
All reactions
  * 👍 126 reactions
  * 😄 15 reactions
  * 🎉 37 reactions
  * ❤️ 55 reactions
  * 🚀 20 reactions
  * 👀 17 reactions

192 people reacted
## openclaw 2026.3.22
23 Mar 11:11
![@steipete](https://avatars.githubusercontent.com/u/58493?s=40&v=4) [steipete](https://github.com/steipete)
[ v2026.3.22  ](https://github.com/openclaw/openclaw/tree/v2026.3.22)
This tag was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
[ `e7d11f6`](https://github.com/openclaw/openclaw/commit/e7d11f6c33e223a0dd8a21cfe01076bd76cef87a)
This commit was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
Compare
#  Choose a tag to compare
## Sorry, something went wrong.
Filter
Loading
## Sorry, something went wrong.
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
## No results found
[View all tags](https://github.com/openclaw/openclaw/tags)
[openclaw 2026.3.22](https://github.com/openclaw/openclaw/releases/tag/v2026.3.22)
## 2026.3.22
### Breaking
  * Plugins/install: bare `openclaw plugins install <package>` now prefers ClawHub before npm for npm-safe names, and only falls back to npm when ClawHub does not have that package or version. Docs: <https://docs.openclaw.ai/tools/clawhub>
  * Browser/Chrome MCP: remove the legacy Chrome extension relay path, bundled extension assets, `driver: "extension"`, and `browser.relayBindHost`. Run `openclaw doctor --fix` to migrate host-local browser config to `existing-session` / `user`; Docker, headless, sandbox, and remote browser flows still use raw CDP. Docs: <https://docs.openclaw.ai/gateway/doctor> and <https://docs.openclaw.ai/tools/browser> ([#47893](https://github.com/openclaw/openclaw/pull/47893)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Tools/image generation: standardize the stock image create/edit path on the core `image_generate` tool. The old `nano-banana-pro` docs/examples are gone; if you previously copied that sample-skill config, switch to `agents.defaults.imageGenerationModel` for built-in image generation or install a separate third-party skill explicitly.
  * Skills/image generation: remove the bundled `nano-banana-pro` skill wrapper. Use `agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"` for the native Nano Banana-style path instead.
  * Plugins/SDK: the new public plugin SDK surface is `openclaw/plugin-sdk/*`; `openclaw/extension-api` is removed with no compatibility shim. Bundled plugins must use injected runtime for host-side operations (for example `api.runtime.agent.runEmbeddedPiAgent`) and any remaining direct imports must come from narrow `openclaw/plugin-sdk/*` subpaths instead of the monolithic SDK root. Docs: <https://docs.openclaw.ai/plugins/sdk-migration> and <https://docs.openclaw.ai/plugins/sdk-overview>
  * Plugins/message discovery: require `ChannelMessageActionAdapter.describeMessageTool(...)` for shared `message` tool discovery. The legacy `listActions`, `getCapabilities`, and `getToolSchema` adapter methods are removed. Plugin authors should migrate message discovery to `describeMessageTool(...)` and keep channel-specific action runtime code inside the owning plugin package. Thanks [@gumadeiras](https://github.com/gumadeiras).
  * Plugins/Matrix: add a new Matrix plugin backed by the official `matrix-js-sdk`. If you are upgrading from the previous public Matrix plugin, follow the migration guide: <https://docs.openclaw.ai/install/migrating-matrix> Thanks [@gumadeiras](https://github.com/gumadeiras).
  * Config/env: remove legacy `CLAWDBOT_*` and `MOLTBOT_*` compatibility env names across runtime, installers, and test tooling. Use the matching `OPENCLAW_*` env names instead.
  * Config/state: remove legacy `.moltbot` state-dir and `moltbot.json` auto-detection/migration fallback. If you still keep state under `~/.moltbot`, move it to `~/.openclaw` or set `OPENCLAW_STATE_DIR` / `OPENCLAW_CONFIG_PATH` explicitly. Docs: <https://docs.openclaw.ai/install/migrating> and <https://docs.openclaw.ai/start/getting-started>
  * Exec/env sandbox: block build-tool JVM injection (`MAVEN_OPTS`, `SBT_OPTS`, `GRADLE_OPTS`, `ANT_OPTS`), glibc tunable exploitation (`GLIBC_TUNABLES`), and .NET dependency resolution hijack (`DOTNET_ADDITIONAL_DEPS`) from the host exec environment, and restrict Gradle init script redirect (`GRADLE_USER_HOME`) as an override-only block so user-configured Gradle homes still propagate. ([#49702](https://github.com/openclaw/openclaw/pull/49702))
  * Discord/commands: switch native command deployment to Carbon reconcile by default so Discord restarts stop churning slash commands through OpenClaw’s local deploy path. ([#46597](https://github.com/openclaw/openclaw/pull/46597)) Thanks [@huntharo](https://github.com/huntharo) and [@thewilloftheshadow](https://github.com/thewilloftheshadow).
  * Security/exec approvals: treat `time` as a transparent dispatch wrapper during allowlist evaluation and allow-always persistence so approved `time ...` commands bind the inner executable instead of the wrapper path. Thanks [@YLChen-007](https://github.com/YLChen-007) for reporting.
  * Voice-call/webhooks: reject missing provider signature headers before body reads, drop the pre-auth body budget to `64 KB` / `5s`, and cap concurrent pre-auth requests per source IP so unauthenticated callers cannot force the old `1 MB` / `30s` buffering path. Thanks [@SEORY0](https://github.com/SEORY0) for reporting.
  * Plugins/Matrix: stop mention-gated or otherwise dropped room chatter from refreshing focused thread bindings before the message is actually routed, so idle ACP and session bindings can still expire normally in mention-required rooms. Thanks [@vincentkoc](https://github.com/vincentkoc), [@dinakars777](https://github.com/dinakars777) and [@mvanhorn](https://github.com/mvanhorn).
  * Plugins/Matrix: durably dedupe inbound room events across gateway restarts so previously handled Matrix messages are not replayed as new, while preserving clean-restart backlog delivery for unseen events. ([#50922](https://github.com/openclaw/openclaw/pull/50922)) thanks [@gumadeiras](https://github.com/gumadeiras)
  * Agents/media replies: migrate the remaining browser, canvas, and nodes snapshot outputs onto `details.media` so generated media keeps attaching to assistant replies after the collect-then-attach refactor. ([#51731](https://github.com/openclaw/openclaw/pull/51731)) Thanks [@christianklotz](https://github.com/christianklotz).
  * Android/contacts search: escape literal `%` and `_` in contact-name queries so searches like `100%` or `_id` no longer match unrelated contacts through SQL `LIKE` wildcards. ([#41891](https://github.com/openclaw/openclaw/pull/41891)) Thanks [@Kaneki-x](https://github.com/Kaneki-x).
  * Gateway/usage: include reset and deleted archived session transcripts in usage totals, session discovery, and archived-only session detail fallback so the Usage view no longer undercounts rotated sessions. ([#43215](https://github.com/openclaw/openclaw/pull/43215)) Thanks [@rcrick](https://github.com/rcrick).

### Changes
  * ClawHub/install: add native `openclaw skills search|install|update` flows plus `openclaw plugins install clawhub:<package>` with tracked update metadata, gateway skill-install/update support for ClawHub-backed requests, and regression coverage/docs for the new source path.
  * Plugins/marketplaces: add Claude marketplace registry resolution, `plugin@marketplace` installs, marketplace listing, and update support, plus Docker E2E coverage for local and official marketplace flows. ([#48058](https://github.com/openclaw/openclaw/pull/48058)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Commands/plugins: add owner-gated `/plugins` and `/plugin` chat commands for plugin list/show and enable/disable flows, alongside explicit `commands.plugins` config gating. Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Install/update: allow package-manager installs from GitHub `main` via `openclaw update --tag main`, installer `--version main`, or direct npm/pnpm git specs. ([#47630](https://github.com/openclaw/openclaw/pull/47630)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Plugins/bundles: add compatible Codex, Claude, and Cursor bundle discovery/install support, map bundle skills into OpenClaw skills, and apply Claude bundle `settings.json` defaults to embedded Pi with shell overrides sanitized.
  * CLI/hooks: route hook-pack install and update through `openclaw plugins`, keep `openclaw hooks` focused on hook visibility and per-hook controls, and show plugin-managed hook details in CLI output.
  * Models/OpenAI: switch the default OpenAI setup model to `openai/gpt-5.4`, keep Codex on `openai-codex/gpt-5.4`, and centralize OpenAI chat, image, TTS, transcription, and embedding defaults in one shared module so future default-model updates stay low-churn. Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Agents: add per-agent thinking/reasoning/fast defaults and auto-revert disallowed model overrides to the agent's default selection. Thanks [@xuanmingguo](https://github.com/xuanmingguo) and [@vincentkoc](https://github.com/vincentkoc).
  * Commands/btw: add `/btw` side questions for quick tool-less answers about the current session without changing future session context, with dismissible in-session TUI answers and explicit BTW replies on external channels. ([#45444](https://github.com/openclaw/openclaw/pull/45444)) Thanks [@ngutman](https://github.com/ngutman).
  * Sandbox/runtime: add pluggable sandbox backends, ship an OpenShell backend with `mirror` and `remote` workspace modes, and make sandbox list/recreate/prune backend-aware instead of Docker-only.
  * Sandbox/SSH: add a core SSH sandbox backend with secret-backed key, certificate, and known_hosts inputs, move shared remote exec/filesystem tooling into core, and keep OpenShell focused on sandbox lifecycle plus optional `mirror` mode.
  * Browser/existing-session: support `browser.profiles.<name>.userDataDir` so Chrome DevTools MCP can attach to Brave, Edge, and other Chromium-based browsers through their own user data directories. ([#48170](https://github.com/openclaw/openclaw/pull/48170)) Thanks [@velvet-shark](https://github.com/velvet-shark).
  * Plugins/bundles: make enabled bundle MCP servers expose runnable tools in embedded Pi, and default relative bundle MCP launches to the bundle root so marketplace bundles like Context7 work through Pi instead of stopping at config import.
  * Plugins/providers: move OpenRouter, GitHub Copilot, and OpenAI Codex provider/runtime logic into bundled plugins, including dynamic model fallback, runtime auth exchange, stream wrappers, capability hints, and cache-TTL policy.
  * Models/Anthropic Vertex: add core `anthropic-vertex` provider support for Claude via Google Vertex AI, including GCP auth/discovery and main run-path routing. ([#43356](https://github.com/openclaw/openclaw/pull/43356)) Thanks [@sallyom](https://github.com/sallyom) and [@yossiovadia](https://github.com/yossiovadia).
  * Plugins/Chutes: add a bundled Chutes provider with plugin-owned OAuth/API-key auth, dynamic model discovery, and default-on extension wiring. ([#41416](https://github.com/openclaw/openclaw/pull/41416)) Thanks [@Veightor](https://github.com/Veightor).
  * Web tools/Exa: add Exa as a bundled web-search plugin with Exa-native date filters, search-mode selection, and optional content extraction under `plugins.entries.exa.config.webSearch.*`. Thanks [@V-Gutierrez](https://github.com/V-Gutierrez) and [@vincentkoc](https://github.com/vincentkoc).
  * Web tools/Tavily: add Tavily as a bundled web-search provider with dedicated `tavily_search` and `tavily_extract` tools, using canonical plugin-owned config under `plugins.entries.tavily.config.webSearch.*`. ([#49200](https://github.com/openclaw/openclaw/pull/49200)) thanks [@lakshyaag-tavily](https://github.com/lakshyaag-tavily).
  * Web tools/Firecrawl: add Firecrawl as an `onboard`/configure search provider via a bundled plugin, expose explicit `firecrawl_search` and `firecrawl_scrape` tools, and align core `web_fetch` fallback behavior with Firecrawl base-URL/env fallback plus guarded endpoint fetches.
  * Models/OpenAI: add native forward-compat support for `gpt-5.4-mini` and `gpt-5.4-nano` in the OpenAI provider catalog, runtime resolution, and reasoning capability gates. Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Control UI/chat: add an expand-to-canvas button on assistant chat bubbles and in-app session navigation from Sessions and Cron views. Thanks [@BunsDev](https://github.com/BunsDev).
  * Control UI/appearance: unify theme border radii across Claw, Knot, and Dash, and add a Roundness...

[Read more](https://github.com/openclaw/openclaw/releases/tag/v2026.3.22)
### Contributors
  * [ ![@vincentkoc](https://avatars.githubusercontent.com/u/25068?s=64&v=4) ](https://github.com/vincentkoc)
  * [ ![@steipete](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete)
  * [ ![@christianklotz](https://avatars.githubusercontent.com/u/69443?s=64&v=4) ](https://github.com/christianklotz)
  * [ ![@velvet-shark](https://avatars.githubusercontent.com/u/126378?s=64&v=4) ](https://github.com/velvet-shark)
  * [ ![@psacc](https://avatars.githubusercontent.com/u/171010?s=64&v=4) ](https://github.com/psacc)
  * [ ![@mvanhorn](https://avatars.githubusercontent.com/u/455140?s=64&v=4) ](https://github.com/mvanhorn)
  * [ ![@nszhsl](https://avatars.githubusercontent.com/u/512639?s=64&v=4) ](https://github.com/nszhsl)
  * [ ![@jalehman](https://avatars.githubusercontent.com/u/550978?s=64&v=4) ](https://github.com/jalehman)
  * [ ![@Takhoffman](https://avatars.githubusercontent.com/u/781889?s=64&v=4) ](https://github.com/Takhoffman)
  * [ ![@joshavant](https://avatars.githubusercontent.com/u/830519?s=64&v=4) ](https://github.com/joshavant)
  * [ ![@zpbrent](https://avatars.githubusercontent.com/u/834641?s=64&v=4) ](https://github.com/zpbrent)
  * [ ![@sibbl](https://avatars.githubusercontent.com/u/866535?s=64&v=4) ](https://github.com/sibbl)
  * [ ![@Lukavyi](https://avatars.githubusercontent.com/u/1013690?s=64&v=4) ](https://github.com/Lukavyi)
  * [ ![@jarimustonen](https://avatars.githubusercontent.com/u/1272053?s=64&v=4) ](https://github.com/jarimustonen)
  * [ ![@karanuppal](https://avatars.githubusercontent.com/u/1457892?s=64&v=4) ](https://github.com/karanuppal)
  * [ ![@ngutman](https://avatars.githubusercontent.com/u/1540134?s=64&v=4) ](https://github.com/ngutman)
  * [ ![@yossiovadia](https://avatars.githubusercontent.com/u/1851728?s=64&v=4) ](https://github.com/yossiovadia)
  * [ ![@merc1305](https://avatars.githubusercontent.com/u/2715765?s=64&v=4) ](https://github.com/merc1305)
  * [ ![@keshav55](https://avatars.githubusercontent.com/u/3821985?s=64&v=4) ](https://github.com/keshav55)
  * [ ![@snese](https://avatars.githubusercontent.com/u/4168002?s=64&v=4) ](https://github.com/snese)
  * [ ![@yiShanXin](https://avatars.githubusercontent.com/u/4454144?s=64&v=4) ](https://github.com/yiShanXin)
  * [ ![@RichardCao](https://avatars.githubusercontent.com/u/4612401?s=64&v=4) ](https://github.com/RichardCao)
  * [ ![@asyncjason](https://avatars.githubusercontent.com/u/4665758?s=64&v=4) ](https://github.com/asyncjason)
  * [ ![@p3nchan](https://avatars.githubusercontent.com/u/5032148?s=64&v=4) ](https://github.com/p3nchan)
  * [ ![@ademczuk](https://avatars.githubusercontent.com/u/5212682?s=64&v=4) ](https://github.com/ademczuk)
  * [ ![@kunalk16](https://avatars.githubusercontent.com/u/5303824?s=64&v=4) ](https://github.com/kunalk16)
  * [ ![@goweii](https://avatars.githubusercontent.com/u/5456892?s=64&v=4) ](https://github.com/goweii)
  * [ ![@gumadeiras](https://avatars.githubusercontent.com/u/5599352?s=64&v=4) ](https://github.com/gumadeiras)
  * [ ![@huntharo](https://avatars.githubusercontent.com/u/5617868?s=64&v=4) ](https://github.com/huntharo)
  * [ ![@dongzhenye](https://avatars.githubusercontent.com/u/5765843?s=64&v=4) ](https://github.com/dongzhenye)
  * [ ![@GodsBoy](https://avatars.githubusercontent.com/u/5792287?s=64&v=4) ](https://github.com/GodsBoy)
  * [ ![@BruceMacD](https://avatars.githubusercontent.com/u/5853428?s=64&v=4) ](https://github.com/BruceMacD)
  * [ ![@joeykrug](https://avatars.githubusercontent.com/u/5925937?s=64&v=4) ](https://github.com/joeykrug)
  * [ ![@MonkeyLeeT](https://avatars.githubusercontent.com/u/6754057?s=64&v=4) ](https://github.com/MonkeyLeeT)
  * [ ![@tdjackey](https://avatars.githubusercontent.com/u/6791132?s=64&v=4) ](https://github.com/tdjackey)
  * [ ![@Kaneki-x](https://avatars.githubusercontent.com/u/6857108?s=64&v=4) ](https://github.com/Kaneki-x)
  * [ ![@hclsys](https://avatars.githubusercontent.com/u/7755017?s=64&v=4) ](https://github.com/hclsys)
  * [ ![@lixuankai](https://avatars.githubusercontent.com/u/8060486?s=64&v=4) ](https://github.com/lixuankai)
  * [ ![@odysseus0](https://avatars.githubusercontent.com/u/8635094?s=64&v=4) ](https://github.com/odysseus0)
  * [ ![@jscianna](https://avatars.githubusercontent.com/u/9017016?s=64&v=4) ](https://github.com/jscianna)
  * [ ![@day253](https://avatars.githubusercontent.com/u/9634619?s=64&v=4) ](https://github.com/day253)
  * [ ![@caesargattuso](https://avatars.githubusercontent.com/u/10957907?s=64&v=4) ](https://github.com/caesargattuso)
  * [ ![@sallyom](https://avatars.githubusercontent.com/u/11166065?s=64&v=4) ](https://github.com/sallyom)
  * [ ![@danhdoan](https://avatars.githubusercontent.com/u/12591333?s=64&v=4) ](https://github.com/danhdoan)
  * [ ![@rogerdigital](https://avatars.githubusercontent.com/u/13251150?s=64&v=4) ](https://github.com/rogerdigital)
  * [ ![@ShaunTsai](https://avatars.githubusercontent.com/u/13811075?s=64&v=4) ](https://github.com/ShaunTsai)
  * [ ![@chrishham](https://avatars.githubusercontent.com/u/15249653?s=64&v=4) ](https://github.com/chrishham)
  * [ ![@fmercurio](https://avatars.githubusercontent.com/u/15571697?s=64&v=4) ](https://github.com/fmercurio)
  * [ ![@luzhidong](https://avatars.githubusercontent.com/u/15848762?s=64&v=4) ](https://github.com/luzhidong)
  * [ ![@JonathanJing](https://avatars.githubusercontent.com/u/17068507?s=64&v=4) ](https://github.com/JonathanJing)
  * [ ![@CharZhou](https://avatars.githubusercontent.com/u/17255546?s=64&v=4) ](https://github.com/CharZhou)
  * [ ![@7inspire](https://avatars.githubusercontent.com/u/18145066?s=64&v=4) ](https://github.com/7inspire)
  * [ ![@jrrcdev](https://avatars.githubusercontent.com/u/19454127?s=64&v=4) ](https://github.com/jrrcdev)
  * [ ![@obviyus](https://avatars.githubusercontent.com/u/22031114?s=64&v=4) ](https://github.com/obviyus)
  * [ ![@rcrick](https://avatars.githubusercontent.com/u/23069968?s=64&v=4) ](https://github.com/rcrick)
  * [ ![@tomsun28](https://avatars.githubusercontent.com/u/24788200?s=64&v=4) ](https://github.com/tomsun28)
  * [ ![@Jaaneek](https://avatars.githubusercontent.com/u/25470423?s=64&v=4) ](https://github.com/Jaaneek)
  * [ ![@MoerAI](https://avatars.githubusercontent.com/u/26067127?s=64&v=4) ](https://github.com/MoerAI)
  * [ ![@ernestodeoliveira](https://avatars.githubusercontent.com/u/26804139?s=64&v=4) ](https://github.com/ernestodeoliveira)
  * [ ![@Cypherm](https://avatars.githubusercontent.com/u/28184436?s=64&v=4) ](https://github.com/Cypherm)
  * [ ![@Br1an67](https://avatars.githubusercontent.com/u/29810238?s=64&v=4) ](https://github.com/Br1an67)
  * [ ![@YLChen-007](https://avatars.githubusercontent.com/u/30854794?s=64&v=4) ](https://github.com/YLChen-007)
  * [ ![@liyuan97](https://avatars.githubusercontent.com/u/33855278?s=64&v=4) ](https://github.com/liyuan97)
  * [ ![@thewilloftheshadow](https://avatars.githubusercontent.com/u/35580099?s=64&v=4) ](https://github.com/thewilloftheshadow)
  * [ ![@sliverp](https://avatars.githubusercontent.com/u/38134380?s=64&v=4) ](https://github.com/sliverp)
  * [ ![@cgdusek](https://avatars.githubusercontent.com/u/38732970?s=64&v=4) ](https://github.com/cgdusek)
  * [ ![@gladiator9797](https://avatars.githubusercontent.com/u/38899223?s=64&v=4) ](https://github.com/gladiator9797)
  * [ ![@lml2468](https://avatars.githubusercontent.com/u/39320777?s=64&v=4) ](https://github.com/lml2468)
  * [ ![@artwalker](https://avatars.githubusercontent.com/u/44759507?s=64&v=4) ](https://github.com/artwalker)
  * [ ![@Veightor](https://avatars.githubusercontent.com/u/47860869?s=64&v=4) ](https://github.com/Veightor)
  * [ ![@Coobiw](https://avatars.githubusercontent.com/u/48615375?s=64&v=4) ](https://github.com/Coobiw)
  * [ ![@DJjjjhao](https://avatars.githubusercontent.com/u/50042705?s=64&v=4) ](https://github.com/DJjjjhao)
  * [ ![@yassinebkr](https://avatars.githubusercontent.com/u/50209930?s=64&v=4) ](https://github.com/yassinebkr)
  * [ ![@ItsAditya-xyz](https://avatars.githubusercontent.com/u/55331140?s=64&v=4) ](https://github.com/ItsAditya-xyz)
  * [ ![@sahancava](https://avatars.githubusercontent.com/u/57447079?s=64&v=4) ](https://github.com/sahancava)
  * [ ![@V-Gutierrez](https://avatars.githubusercontent.com/u/62355596?s=64&v=4) ](https://github.com/V-Gutierrez)
  * [ ![@git-jxj](https://avatars.githubusercontent.com/u/65210887?s=64&v=4) ](https://github.com/git-jxj)
  * [ ![@BunsDev](https://avatars.githubusercontent.com/u/68980965?s=64&v=4) ](https://github.com/BunsDev)
  * [ ![@meng-clb](https://avatars.githubusercontent.com/u/77823860?s=64&v=4) ](https://github.com/meng-clb)
  * [ ![@RacerZ-fighting](https://avatars.githubusercontent.com/u/78632303?s=64&v=4) ](https://github.com/RacerZ-fighting)
  * [ ![@zidongdesign](https://avatars.githubusercontent.com/u/81469543?s=64&v=4) ](https://github.com/zidongdesign)
  * [ ![@No898](https://avatars.githubusercontent.com/u/82420070?s=64&v=4) ](https://github.com/No898)
  * [ ![@kuranikaran](https://avatars.githubusercontent.com/u/85026744?s=64&v=4) ](https://github.com/kuranikaran)
  * [ ![@thirumaleshp](https://avatars.githubusercontent.com/u/85149081?s=64&v=4) ](https://github.com/thirumaleshp)
  * [ ![@ImLukeF](https://avatars.githubusercontent.com/u/92253590?s=64&v=4) ](https://github.com/ImLukeF)
  * [ ![@SEORY0](https://avatars.githubusercontent.com/u/93699099?s=64&v=4) ](https://github.com/SEORY0)
  * [ ![@Matthew19990919](https://avatars.githubusercontent.com/u/97017241?s=64&v=4) ](https://github.com/Matthew19990919)
  * [ ![@kevinheinrichs](https://avatars.githubusercontent.com/u/113271657?s=64&v=4) ](https://github.com/kevinheinrichs)
  * [ ![@rstar327](https://avatars.githubusercontent.com/u/114364448?s=64&v=4) ](https://github.com/rstar327)
  * [ ![@restriction](https://avatars.githubusercontent.com/u/114768995?s=64&v=4) ](https://github.com/restriction)
  * [ ![@adhitShet](https://avatars.githubusercontent.com/u/131381638?s=64&v=4) ](https://github.com/adhitShet)
  * [ ![@CodeForgeNet](https://avatars.githubusercontent.com/u/166907114?s=64&v=4) ](https://github.com/CodeForgeNet)
  * [ ![@scoootscooob](https://avatars.githubusercontent.com/u/167050519?s=64&v=4) ](https://github.com/scoootscooob)
  * [ ![@tylerliu612](https://avatars.githubusercontent.com/u/179897207?s=64&v=4) ](https://github.com/tylerliu612)
  * [ ![@juliabush](https://avatars.githubusercontent.com/u/187550546?s=64&v=4) ](https://github.com/juliabush)
  * [ ![@ecohash-co](https://avatars.githubusercontent.com/u/191814220?s=64&v=4) ](https://github.com/ecohash-co)
  * [ ![@Pandadadadazxf](https://avatars.githubusercontent.com/u/200469161?s=64&v=4) ](https://github.com/Pandadadadazxf)
  * [ ![@ijxpwastaken](https://avatars.githubusercontent.com/u/234084080?s=64&v=4) ](https://github.com/ijxpwastaken)
  * [ ![@sudie-codes](https://avatars.githubusercontent.com/u/240354752?s=64&v=4) ](https://github.com/sudie-codes)
  * [ ![@dinakars777](https://avatars.githubusercontent.com/u/250428393?s=64&v=4) ](https://github.com/dinakars777)
  * [ ![@cash-echo-bot](https://avatars.githubusercontent.com/u/252747386?s=64&v=4) ](https://github.com/cash-echo-bot)
  * [ ![@brokemac79](https://avatars.githubusercontent.com/u/255583030?s=64&v=4) ](https://github.com/brokemac79)
  * [ ![@xuanmingguo](https://avatars.githubusercontent.com/u/258405939?s=64&v=4) ](https://github.com/xuanmingguo)
  * [ ![@moltbot886](https://avatars.githubusercontent.com/u/258897563?s=64&v=4) ](https://github.com/moltbot886)
  * [ ![@stablegenius49](https://avatars.githubusercontent.com/u/259448942?s=64&v=4) ](https://github.com/stablegenius49)
  * [ ![@Bartok9](https://avatars.githubusercontent.com/u/259807879?s=64&v=4) ](https://github.com/Bartok9)
  * [ ![@claw-sylphx](https://avatars.githubusercontent.com/u/260243939?s=64&v=4) ](https://github.com/claw-sylphx)
  * [ ![@theo674](https://avatars.githubusercontent.com/u/261068216?s=64&v=4) ](https://github.com/theo674)
  * [ ![@clawdia67](https://avatars.githubusercontent.com/u/261743618?s=64&v=4) ](https://github.com/clawdia67)
  * [ ![@thepagent](https://avatars.githubusercontent.com/u/262003297?s=64&v=4) ](https://github.com/thepagent)
  * [ ![@pdd-cli](https://avatars.githubusercontent.com/u/262266283?s=64&v=4) ](https://github.com/pdd-cli)
  * [ ![@fuller-stack-dev](https://avatars.githubusercontent.com/u/263060202?s=64&v=4) ](https://github.com/fuller-stack-dev)
  * [ ![@martingarramon](https://avatars.githubusercontent.com/u/263922628?s=64&v=4) ](https://github.com/martingarramon)
  * [ ![@xaeon2026](https://avatars.githubusercontent.com/u/264572156?s=64&v=4) ](https://github.com/xaeon2026)
  * [ ![@lakshyaag-tavily](https://avatars.githubusercontent.com/u/266572148?s=64&v=4) ](https://github.com/lakshyaag-tavily)
  * [ ![@smaeljaish771](https://avatars.githubusercontent.com/u/266604088?s=64&v=4) ](https://github.com/smaeljaish771)
  * [ ![@Alix-007](https://avatars.githubusercontent.com/u/267018309?s=64&v=4) ](https://github.com/Alix-007)
  * [ ![@bobBot-claw](https://avatars.githubusercontent.com/u/268404736?s=64&v=4) ](https://github.com/bobBot-claw)
  * [ ![@nexrin](https://avatars.githubusercontent.com/u/268879349?s=64&v=4) ](https://github.com/nexrin)
  * [ ![@oliviareid-svg](https://avatars.githubusercontent.com/u/269669958?s=64&v=4) ](https://github.com/oliviareid-svg)

vincentkoc, steipete, and 118 other contributors
Assets 2
Loading
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
👍 157 dev-Kanade, nhmpk824-gif, lsyuuk, nakheel77, tdjackey, Junvate, SirBrother, j0KZ, robbyzhaox, Eskyee, and 147 more reacted with thumbs up emoji 😄 26 orwiso, Esperadoce, lin72h, artwalker, iliuyi, Cabal-312512, bwlfhu, Ruslan0990, xbsheng, AgatElite, and 16 more reacted with laugh emoji 🎉 40 nhmpk824-gif, jokedul, lsyuuk, Eskyee, goiltpatpat, orwiso, ilne, artwalker, brandonvers, proelkady, and 30 more reacted with hooray emoji ❤️ 43 Eskyee, goiltpatpat, jame25, orwiso, lin72h, artwalker, brandonvers, KamilBeda, 3koozy, Nellumbo, and 33 more reacted with heart emoji 🚀 32 jokedul, lsyuuk, Eskyee, goiltpatpat, orwiso, lin72h, artwalker, brandonvers, 3koozy, Duncandowne, and 22 more reacted with rocket emoji 👀 29 jokedul, Eskyee, orwiso, Puiching-Memory, artwalker, bwlfhu, xbsheng, YuXilong, AgatElite, wangyq100, and 19 more reacted with eyes emoji
All reactions
  * 👍 157 reactions
  * 😄 26 reactions
  * 🎉 40 reactions
  * ❤️ 43 reactions
  * 🚀 32 reactions
  * 👀 29 reactions

214 people reacted
## openclaw 2026.3.22-beta.1
23 Mar 09:37
![@steipete](https://avatars.githubusercontent.com/u/58493?s=40&v=4) [steipete](https://github.com/steipete)
Immutable release. Only release title and notes can be modified.
[ v2026.3.22-beta.1  ](https://github.com/openclaw/openclaw/tree/v2026.3.22-beta.1)
This tag was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
[ `d8d545b`](https://github.com/openclaw/openclaw/commit/d8d545bac1ee36078a3c2e5e8c85b92456e7423f)
This commit was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
Compare
#  Choose a tag to compare
## Sorry, something went wrong.
Filter
Loading
## Sorry, something went wrong.
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
## No results found
[View all tags](https://github.com/openclaw/openclaw/tags)
[openclaw 2026.3.22-beta.1](https://github.com/openclaw/openclaw/releases/tag/v2026.3.22-beta.1) Pre-release
Pre-release
Pre-release for npm beta tag `v2026.3.22-beta.1`.
No new macOS app build is attached to this beta. macOS assets remain on stable app version `2026.3.22`, and `appcast.xml` is intentionally unchanged in this pre-release.
### Breaking
  * Plugins/install: bare `openclaw plugins install <package>` now prefers ClawHub before npm for npm-safe names, and only falls back to npm when ClawHub does not have that package or version. Docs: <https://docs.openclaw.ai/tools/clawhub>
  * Browser/Chrome MCP: remove the legacy Chrome extension relay path, bundled extension assets, `driver: "extension"`, and `browser.relayBindHost`. Run `openclaw doctor --fix` to migrate host-local browser config to `existing-session` / `user`; Docker, headless, sandbox, and remote browser flows still use raw CDP. Docs: <https://docs.openclaw.ai/gateway/doctor> and <https://docs.openclaw.ai/tools/browser> ([#47893](https://github.com/openclaw/openclaw/pull/47893)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Tools/image generation: standardize the stock image create/edit path on the core `image_generate` tool. The old `nano-banana-pro` docs/examples are gone; if you previously copied that sample-skill config, switch to `agents.defaults.imageGenerationModel` for built-in image generation or install a separate third-party skill explicitly.
  * Skills/image generation: remove the bundled `nano-banana-pro` skill wrapper. Use `agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"` for the native Nano Banana-style path instead.
  * Plugins/SDK: the new public plugin SDK surface is `openclaw/plugin-sdk/*`; `openclaw/extension-api` is removed with no compatibility shim. Bundled plugins must use injected runtime for host-side operations (for example `api.runtime.agent.runEmbeddedPiAgent`) and any remaining direct imports must come from narrow `openclaw/plugin-sdk/*` subpaths instead of the monolithic SDK root. Docs: <https://docs.openclaw.ai/plugins/sdk-migration> and <https://docs.openclaw.ai/plugins/sdk-overview>
  * Plugins/message discovery: require `ChannelMessageActionAdapter.describeMessageTool(...)` for shared `message` tool discovery. The legacy `listActions`, `getCapabilities`, and `getToolSchema` adapter methods are removed. Plugin authors should migrate message discovery to `describeMessageTool(...)` and keep channel-specific action runtime code inside the owning plugin package. Thanks [@gumadeiras](https://github.com/gumadeiras).
  * Plugins/Matrix: add a new Matrix plugin backed by the official `matrix-js-sdk`. If you are upgrading from the previous public Matrix plugin, follow the migration guide: <https://docs.openclaw.ai/install/migrating-matrix> Thanks [@gumadeiras](https://github.com/gumadeiras).
  * Config/env: remove legacy `CLAWDBOT_*` and `MOLTBOT_*` compatibility env names across runtime, installers, and test tooling. Use the matching `OPENCLAW_*` env names instead.
  * Config/state: remove legacy `.moltbot` state-dir and `moltbot.json` auto-detection/migration fallback. If you still keep state under `~/.moltbot`, move it to `~/.openclaw` or set `OPENCLAW_STATE_DIR` / `OPENCLAW_CONFIG_PATH` explicitly. Docs: <https://docs.openclaw.ai/install/migrating> and <https://docs.openclaw.ai/start/getting-started>
  * Exec/env sandbox: block build-tool JVM injection (`MAVEN_OPTS`, `SBT_OPTS`, `GRADLE_OPTS`, `ANT_OPTS`), glibc tunable exploitation (`GLIBC_TUNABLES`), and .NET dependency resolution hijack (`DOTNET_ADDITIONAL_DEPS`) from the host exec environment, and restrict Gradle init script redirect (`GRADLE_USER_HOME`) as an override-only block so user-configured Gradle homes still propagate. ([#49702](https://github.com/openclaw/openclaw/pull/49702))
  * Discord/commands: switch native command deployment to Carbon reconcile by default so Discord restarts stop churning slash commands through OpenClaw’s local deploy path. ([#46597](https://github.com/openclaw/openclaw/pull/46597)) Thanks [@huntharo](https://github.com/huntharo) and [@thewilloftheshadow](https://github.com/thewilloftheshadow).
  * Security/exec approvals: treat `time` as a transparent dispatch wrapper during allowlist evaluation and allow-always persistence so approved `time ...` commands bind the inner executable instead of the wrapper path. Thanks [@YLChen-007](https://github.com/YLChen-007) for reporting.
  * Voice-call/webhooks: reject missing provider signature headers before body reads, drop the pre-auth body budget to `64 KB` / `5s`, and cap concurrent pre-auth requests per source IP so unauthenticated callers cannot force the old `1 MB` / `30s` buffering path. Thanks [@SEORY0](https://github.com/SEORY0) for reporting.
  * Plugins/Matrix: stop mention-gated or otherwise dropped room chatter from refreshing focused thread bindings before the message is actually routed, so idle ACP and session bindings can still expire normally in mention-required rooms. Thanks [@vincentkoc](https://github.com/vincentkoc), [@dinakars777](https://github.com/dinakars777) and [@mvanhorn](https://github.com/mvanhorn).
  * Plugins/Matrix: durably dedupe inbound room events across gateway restarts so previously handled Matrix messages are not replayed as new, while preserving clean-restart backlog delivery for unseen events. ([#50922](https://github.com/openclaw/openclaw/pull/50922)) thanks [@gumadeiras](https://github.com/gumadeiras)
  * Agents/media replies: migrate the remaining browser, canvas, and nodes snapshot outputs onto `details.media` so generated media keeps attaching to assistant replies after the collect-then-attach refactor. ([#51731](https://github.com/openclaw/openclaw/pull/51731)) Thanks [@christianklotz](https://github.com/christianklotz).
  * Android/contacts search: escape literal `%` and `_` in contact-name queries so searches like `100%` or `_id` no longer match unrelated contacts through SQL `LIKE` wildcards. ([#41891](https://github.com/openclaw/openclaw/pull/41891)) Thanks [@Kaneki-x](https://github.com/Kaneki-x).
  * Gateway/usage: include reset and deleted archived session transcripts in usage totals, session discovery, and archived-only session detail fallback so the Usage view no longer undercounts rotated sessions. ([#43215](https://github.com/openclaw/openclaw/pull/43215)) Thanks [@rcrick](https://github.com/rcrick).

### Changes
  * ClawHub/install: add native `openclaw skills search|install|update` flows plus `openclaw plugins install clawhub:<package>` with tracked update metadata, gateway skill-install/update support for ClawHub-backed requests, and regression coverage/docs for the new source path.
  * Plugins/marketplaces: add Claude marketplace registry resolution, `plugin@marketplace` installs, marketplace listing, and update support, plus Docker E2E coverage for local and official marketplace flows. ([#48058](https://github.com/openclaw/openclaw/pull/48058)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Commands/plugins: add owner-gated `/plugins` and `/plugin` chat commands for plugin list/show and enable/disable flows, alongside explicit `commands.plugins` config gating. Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Install/update: allow package-manager installs from GitHub `main` via `openclaw update --tag main`, installer `--version main`, or direct npm/pnpm git specs. ([#47630](https://github.com/openclaw/openclaw/pull/47630)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Plugins/bundles: add compatible Codex, Claude, and Cursor bundle discovery/install support, map bundle skills into OpenClaw skills, and apply Claude bundle `settings.json` defaults to embedded Pi with shell overrides sanitized.
  * CLI/hooks: route hook-pack install and update through `openclaw plugins`, keep `openclaw hooks` focused on hook visibility and per-hook controls, and show plugin-managed hook details in CLI output.
  * Models/OpenAI: switch the default OpenAI setup model to `openai/gpt-5.4`, keep Codex on `openai-codex/gpt-5.4`, and centralize OpenAI chat, image, TTS, transcription, and embedding defaults in one shared module so future default-model updates stay low-churn. Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Agents: add per-agent thinking/reasoning/fast defaults and auto-revert disallowed model overrides to the agent's default selection. Thanks [@xuanmingguo](https://github.com/xuanmingguo) and [@vincentkoc](https://github.com/vincentkoc).
  * Commands/btw: add `/btw` side questions for quick tool-less answers about the current session without changing future session context, with dismissible in-session TUI answers and explicit BTW replies on external channels. ([#45444](https://github.com/openclaw/openclaw/pull/45444)) Thanks [@ngutman](https://github.com/ngutman).
  * Sandbox/runtime: add pluggable sandbox backends, ship an OpenShell backend with `mirror` and `remote` workspace modes, and make sandbox list/recreate/prune backend-aware instead of Docker-only.
  * Sandbox/SSH: add a core SSH sandbox backend with secret-backed key, certificate, and known_hosts inputs, move shared remote exec/filesystem tooling into core, and keep OpenShell focused on sandbox lifecycle plus optional `mirror` mode.
  * Browser/existing-session: support `browser.profiles.<name>.userDataDir` so Chrome DevTools MCP can attach to Brave, Edge, and other Chromium-based browsers through their own user data directories. ([#48170](https://github.com/openclaw/openclaw/pull/48170)) Thanks [@velvet-shark](https://github.com/velvet-shark).
  * Plugins/bundles: make enabled bundle MCP servers expose runnable tools in embedded Pi, and default relative bundle MCP launches to the bundle root so marketplace bundles like Context7 work through Pi instead of stopping at config import.
  * Plugins/providers: move OpenRouter, GitHub Copilot, and OpenAI Codex provider/runtime logic into bundled plugins, including dynamic model fallback, runtime auth exchange, stream wrappers, capability hints, and cache-TTL policy.
  * Models/Anthropic Vertex: add core `anthropic-vertex` provider support for Claude via Google Vertex AI, including GCP auth/discovery and main run-path routing. ([#43356](https://github.com/openclaw/openclaw/pull/43356)) Thanks [@sallyom](https://github.com/sallyom) and [@yossiovadia](https://github.com/yossiovadia).
  * Plugins/Chutes: add a bundled Chutes provider with plugin-owned OAuth/API-key auth, dynamic model discovery, and default-on extension wiring. ([#41416](https://github.com/openclaw/openclaw/pull/41416)) Thanks [@Veightor](https://github.com/Veightor).
  * Web tools/Exa: add Exa as a bundled web-search plugin with Exa-native date filters, search-mode selection, and optional content extraction under `plugins.entries.exa.config.webSearch.*`. Thanks [@V-Gutierrez](https://github.com/V-Gutierrez) and [@vincentkoc](https://github.com/vincentkoc).
  * Web tools/Tavily: add Tavily as a bundled web-search provider with dedicated `tavily_search` and `tavily_extract` tools, using canonical plugin-owned config under `plugins.entries.tavily.config.webSearch.*`. ([#49200](https://github.com/openclaw/openclaw/pull/49200)) thanks [@lakshyaag-tavily](https://github.com/lakshyaag-tavily).
  * Web tools/Firecrawl: add Firecrawl as an `onboard`/configure search provider via a bundled plugin, expose explicit `firecrawl_search` and `firecrawl_scrape` tools, and align core `web_fetch` fallback behavior with Firecrawl base-URL/env fallback plus guarded endpoint fetches.
  * Models/OpenAI: add native forward-compat support for `gpt-5.4-mini` and `gpt-5.4-nano` in the OpenAI provider catalog, runtime resolution, and reasoning capability gates. Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Control UI/chat: add an expand-to-canvas ...

[Read more](https://github.com/openclaw/openclaw/releases/tag/v2026.3.22-beta.1)
### Contributors
  * [ ![@vincentkoc](https://avatars.githubusercontent.com/u/25068?s=64&v=4) ](https://github.com/vincentkoc)
  * [ ![@steipete](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete)
  * [ ![@christianklotz](https://avatars.githubusercontent.com/u/69443?s=64&v=4) ](https://github.com/christianklotz)
  * [ ![@velvet-shark](https://avatars.githubusercontent.com/u/126378?s=64&v=4) ](https://github.com/velvet-shark)
  * [ ![@psacc](https://avatars.githubusercontent.com/u/171010?s=64&v=4) ](https://github.com/psacc)
  * [ ![@mvanhorn](https://avatars.githubusercontent.com/u/455140?s=64&v=4) ](https://github.com/mvanhorn)
  * [ ![@nszhsl](https://avatars.githubusercontent.com/u/512639?s=64&v=4) ](https://github.com/nszhsl)
  * [ ![@jalehman](https://avatars.githubusercontent.com/u/550978?s=64&v=4) ](https://github.com/jalehman)
  * [ ![@Takhoffman](https://avatars.githubusercontent.com/u/781889?s=64&v=4) ](https://github.com/Takhoffman)
  * [ ![@joshavant](https://avatars.githubusercontent.com/u/830519?s=64&v=4) ](https://github.com/joshavant)
  * [ ![@zpbrent](https://avatars.githubusercontent.com/u/834641?s=64&v=4) ](https://github.com/zpbrent)
  * [ ![@sibbl](https://avatars.githubusercontent.com/u/866535?s=64&v=4) ](https://github.com/sibbl)
  * [ ![@Lukavyi](https://avatars.githubusercontent.com/u/1013690?s=64&v=4) ](https://github.com/Lukavyi)
  * [ ![@jarimustonen](https://avatars.githubusercontent.com/u/1272053?s=64&v=4) ](https://github.com/jarimustonen)
  * [ ![@karanuppal](https://avatars.githubusercontent.com/u/1457892?s=64&v=4) ](https://github.com/karanuppal)
  * [ ![@ngutman](https://avatars.githubusercontent.com/u/1540134?s=64&v=4) ](https://github.com/ngutman)
  * [ ![@yossiovadia](https://avatars.githubusercontent.com/u/1851728?s=64&v=4) ](https://github.com/yossiovadia)
  * [ ![@merc1305](https://avatars.githubusercontent.com/u/2715765?s=64&v=4) ](https://github.com/merc1305)
  * [ ![@keshav55](https://avatars.githubusercontent.com/u/3821985?s=64&v=4) ](https://github.com/keshav55)
  * [ ![@snese](https://avatars.githubusercontent.com/u/4168002?s=64&v=4) ](https://github.com/snese)
  * [ ![@yiShanXin](https://avatars.githubusercontent.com/u/4454144?s=64&v=4) ](https://github.com/yiShanXin)
  * [ ![@RichardCao](https://avatars.githubusercontent.com/u/4612401?s=64&v=4) ](https://github.com/RichardCao)
  * [ ![@asyncjason](https://avatars.githubusercontent.com/u/4665758?s=64&v=4) ](https://github.com/asyncjason)
  * [ ![@p3nchan](https://avatars.githubusercontent.com/u/5032148?s=64&v=4) ](https://github.com/p3nchan)
  * [ ![@ademczuk](https://avatars.githubusercontent.com/u/5212682?s=64&v=4) ](https://github.com/ademczuk)
  * [ ![@kunalk16](https://avatars.githubusercontent.com/u/5303824?s=64&v=4) ](https://github.com/kunalk16)
  * [ ![@goweii](https://avatars.githubusercontent.com/u/5456892?s=64&v=4) ](https://github.com/goweii)
  * [ ![@gumadeiras](https://avatars.githubusercontent.com/u/5599352?s=64&v=4) ](https://github.com/gumadeiras)
  * [ ![@huntharo](https://avatars.githubusercontent.com/u/5617868?s=64&v=4) ](https://github.com/huntharo)
  * [ ![@dongzhenye](https://avatars.githubusercontent.com/u/5765843?s=64&v=4) ](https://github.com/dongzhenye)
  * [ ![@GodsBoy](https://avatars.githubusercontent.com/u/5792287?s=64&v=4) ](https://github.com/GodsBoy)
  * [ ![@BruceMacD](https://avatars.githubusercontent.com/u/5853428?s=64&v=4) ](https://github.com/BruceMacD)
  * [ ![@joeykrug](https://avatars.githubusercontent.com/u/5925937?s=64&v=4) ](https://github.com/joeykrug)
  * [ ![@MonkeyLeeT](https://avatars.githubusercontent.com/u/6754057?s=64&v=4) ](https://github.com/MonkeyLeeT)
  * [ ![@tdjackey](https://avatars.githubusercontent.com/u/6791132?s=64&v=4) ](https://github.com/tdjackey)
  * [ ![@Kaneki-x](https://avatars.githubusercontent.com/u/6857108?s=64&v=4) ](https://github.com/Kaneki-x)
  * [ ![@hclsys](https://avatars.githubusercontent.com/u/7755017?s=64&v=4) ](https://github.com/hclsys)
  * [ ![@lixuankai](https://avatars.githubusercontent.com/u/8060486?s=64&v=4) ](https://github.com/lixuankai)
  * [ ![@odysseus0](https://avatars.githubusercontent.com/u/8635094?s=64&v=4) ](https://github.com/odysseus0)
  * [ ![@jscianna](https://avatars.githubusercontent.com/u/9017016?s=64&v=4) ](https://github.com/jscianna)
  * [ ![@day253](https://avatars.githubusercontent.com/u/9634619?s=64&v=4) ](https://github.com/day253)
  * [ ![@caesargattuso](https://avatars.githubusercontent.com/u/10957907?s=64&v=4) ](https://github.com/caesargattuso)
  * [ ![@sallyom](https://avatars.githubusercontent.com/u/11166065?s=64&v=4) ](https://github.com/sallyom)
  * [ ![@danhdoan](https://avatars.githubusercontent.com/u/12591333?s=64&v=4) ](https://github.com/danhdoan)
  * [ ![@rogerdigital](https://avatars.githubusercontent.com/u/13251150?s=64&v=4) ](https://github.com/rogerdigital)
  * [ ![@ShaunTsai](https://avatars.githubusercontent.com/u/13811075?s=64&v=4) ](https://github.com/ShaunTsai)
  * [ ![@chrishham](https://avatars.githubusercontent.com/u/15249653?s=64&v=4) ](https://github.com/chrishham)
  * [ ![@fmercurio](https://avatars.githubusercontent.com/u/15571697?s=64&v=4) ](https://github.com/fmercurio)
  * [ ![@luzhidong](https://avatars.githubusercontent.com/u/15848762?s=64&v=4) ](https://github.com/luzhidong)
  * [ ![@JonathanJing](https://avatars.githubusercontent.com/u/17068507?s=64&v=4) ](https://github.com/JonathanJing)
  * [ ![@CharZhou](https://avatars.githubusercontent.com/u/17255546?s=64&v=4) ](https://github.com/CharZhou)
  * [ ![@7inspire](https://avatars.githubusercontent.com/u/18145066?s=64&v=4) ](https://github.com/7inspire)
  * [ ![@jrrcdev](https://avatars.githubusercontent.com/u/19454127?s=64&v=4) ](https://github.com/jrrcdev)
  * [ ![@obviyus](https://avatars.githubusercontent.com/u/22031114?s=64&v=4) ](https://github.com/obviyus)
  * [ ![@rcrick](https://avatars.githubusercontent.com/u/23069968?s=64&v=4) ](https://github.com/rcrick)
  * [ ![@tomsun28](https://avatars.githubusercontent.com/u/24788200?s=64&v=4) ](https://github.com/tomsun28)
  * [ ![@Jaaneek](https://avatars.githubusercontent.com/u/25470423?s=64&v=4) ](https://github.com/Jaaneek)
  * [ ![@MoerAI](https://avatars.githubusercontent.com/u/26067127?s=64&v=4) ](https://github.com/MoerAI)
  * [ ![@ernestodeoliveira](https://avatars.githubusercontent.com/u/26804139?s=64&v=4) ](https://github.com/ernestodeoliveira)
  * [ ![@Cypherm](https://avatars.githubusercontent.com/u/28184436?s=64&v=4) ](https://github.com/Cypherm)
  * [ ![@Br1an67](https://avatars.githubusercontent.com/u/29810238?s=64&v=4) ](https://github.com/Br1an67)
  * [ ![@YLChen-007](https://avatars.githubusercontent.com/u/30854794?s=64&v=4) ](https://github.com/YLChen-007)
  * [ ![@liyuan97](https://avatars.githubusercontent.com/u/33855278?s=64&v=4) ](https://github.com/liyuan97)
  * [ ![@thewilloftheshadow](https://avatars.githubusercontent.com/u/35580099?s=64&v=4) ](https://github.com/thewilloftheshadow)
  * [ ![@sliverp](https://avatars.githubusercontent.com/u/38134380?s=64&v=4) ](https://github.com/sliverp)
  * [ ![@cgdusek](https://avatars.githubusercontent.com/u/38732970?s=64&v=4) ](https://github.com/cgdusek)
  * [ ![@gladiator9797](https://avatars.githubusercontent.com/u/38899223?s=64&v=4) ](https://github.com/gladiator9797)
  * [ ![@lml2468](https://avatars.githubusercontent.com/u/39320777?s=64&v=4) ](https://github.com/lml2468)
  * [ ![@artwalker](https://avatars.githubusercontent.com/u/44759507?s=64&v=4) ](https://github.com/artwalker)
  * [ ![@Veightor](https://avatars.githubusercontent.com/u/47860869?s=64&v=4) ](https://github.com/Veightor)
  * [ ![@Coobiw](https://avatars.githubusercontent.com/u/48615375?s=64&v=4) ](https://github.com/Coobiw)
  * [ ![@DJjjjhao](https://avatars.githubusercontent.com/u/50042705?s=64&v=4) ](https://github.com/DJjjjhao)
  * [ ![@yassinebkr](https://avatars.githubusercontent.com/u/50209930?s=64&v=4) ](https://github.com/yassinebkr)
  * [ ![@ItsAditya-xyz](https://avatars.githubusercontent.com/u/55331140?s=64&v=4) ](https://github.com/ItsAditya-xyz)
  * [ ![@sahancava](https://avatars.githubusercontent.com/u/57447079?s=64&v=4) ](https://github.com/sahancava)
  * [ ![@V-Gutierrez](https://avatars.githubusercontent.com/u/62355596?s=64&v=4) ](https://github.com/V-Gutierrez)
  * [ ![@git-jxj](https://avatars.githubusercontent.com/u/65210887?s=64&v=4) ](https://github.com/git-jxj)
  * [ ![@BunsDev](https://avatars.githubusercontent.com/u/68980965?s=64&v=4) ](https://github.com/BunsDev)
  * [ ![@meng-clb](https://avatars.githubusercontent.com/u/77823860?s=64&v=4) ](https://github.com/meng-clb)
  * [ ![@RacerZ-fighting](https://avatars.githubusercontent.com/u/78632303?s=64&v=4) ](https://github.com/RacerZ-fighting)
  * [ ![@zidongdesign](https://avatars.githubusercontent.com/u/81469543?s=64&v=4) ](https://github.com/zidongdesign)
  * [ ![@No898](https://avatars.githubusercontent.com/u/82420070?s=64&v=4) ](https://github.com/No898)
  * [ ![@kuranikaran](https://avatars.githubusercontent.com/u/85026744?s=64&v=4) ](https://github.com/kuranikaran)
  * [ ![@thirumaleshp](https://avatars.githubusercontent.com/u/85149081?s=64&v=4) ](https://github.com/thirumaleshp)
  * [ ![@ImLukeF](https://avatars.githubusercontent.com/u/92253590?s=64&v=4) ](https://github.com/ImLukeF)
  * [ ![@SEORY0](https://avatars.githubusercontent.com/u/93699099?s=64&v=4) ](https://github.com/SEORY0)
  * [ ![@Matthew19990919](https://avatars.githubusercontent.com/u/97017241?s=64&v=4) ](https://github.com/Matthew19990919)
  * [ ![@rstar327](https://avatars.githubusercontent.com/u/114364448?s=64&v=4) ](https://github.com/rstar327)
  * [ ![@restriction](https://avatars.githubusercontent.com/u/114768995?s=64&v=4) ](https://github.com/restriction)
  * [ ![@adhitShet](https://avatars.githubusercontent.com/u/131381638?s=64&v=4) ](https://github.com/adhitShet)
  * [ ![@CodeForgeNet](https://avatars.githubusercontent.com/u/166907114?s=64&v=4) ](https://github.com/CodeForgeNet)
  * [ ![@scoootscooob](https://avatars.githubusercontent.com/u/167050519?s=64&v=4) ](https://github.com/scoootscooob)
  * [ ![@tylerliu612](https://avatars.githubusercontent.com/u/179897207?s=64&v=4) ](https://github.com/tylerliu612)
  * [ ![@juliabush](https://avatars.githubusercontent.com/u/187550546?s=64&v=4) ](https://github.com/juliabush)
  * [ ![@ecohash-co](https://avatars.githubusercontent.com/u/191814220?s=64&v=4) ](https://github.com/ecohash-co)
  * [ ![@Pandadadadazxf](https://avatars.githubusercontent.com/u/200469161?s=64&v=4) ](https://github.com/Pandadadadazxf)
  * [ ![@ijxpwastaken](https://avatars.githubusercontent.com/u/234084080?s=64&v=4) ](https://github.com/ijxpwastaken)
  * [ ![@sudie-codes](https://avatars.githubusercontent.com/u/240354752?s=64&v=4) ](https://github.com/sudie-codes)
  * [ ![@dinakars777](https://avatars.githubusercontent.com/u/250428393?s=64&v=4) ](https://github.com/dinakars777)
  * [ ![@cash-echo-bot](https://avatars.githubusercontent.com/u/252747386?s=64&v=4) ](https://github.com/cash-echo-bot)
  * [ ![@brokemac79](https://avatars.githubusercontent.com/u/255583030?s=64&v=4) ](https://github.com/brokemac79)
  * [ ![@xuanmingguo](https://avatars.githubusercontent.com/u/258405939?s=64&v=4) ](https://github.com/xuanmingguo)
  * [ ![@moltbot886](https://avatars.githubusercontent.com/u/258897563?s=64&v=4) ](https://github.com/moltbot886)
  * [ ![@stablegenius49](https://avatars.githubusercontent.com/u/259448942?s=64&v=4) ](https://github.com/stablegenius49)
  * [ ![@Bartok9](https://avatars.githubusercontent.com/u/259807879?s=64&v=4) ](https://github.com/Bartok9)
  * [ ![@claw-sylphx](https://avatars.githubusercontent.com/u/260243939?s=64&v=4) ](https://github.com/claw-sylphx)
  * [ ![@clawdia67](https://avatars.githubusercontent.com/u/261743618?s=64&v=4) ](https://github.com/clawdia67)
  * [ ![@thepagent](https://avatars.githubusercontent.com/u/262003297?s=64&v=4) ](https://github.com/thepagent)
  * [ ![@pdd-cli](https://avatars.githubusercontent.com/u/262266283?s=64&v=4) ](https://github.com/pdd-cli)
  * [ ![@fuller-stack-dev](https://avatars.githubusercontent.com/u/263060202?s=64&v=4) ](https://github.com/fuller-stack-dev)
  * [ ![@martingarramon](https://avatars.githubusercontent.com/u/263922628?s=64&v=4) ](https://github.com/martingarramon)
  * [ ![@xaeon2026](https://avatars.githubusercontent.com/u/264572156?s=64&v=4) ](https://github.com/xaeon2026)
  * [ ![@lakshyaag-tavily](https://avatars.githubusercontent.com/u/266572148?s=64&v=4) ](https://github.com/lakshyaag-tavily)
  * [ ![@smaeljaish771](https://avatars.githubusercontent.com/u/266604088?s=64&v=4) ](https://github.com/smaeljaish771)
  * [ ![@Alix-007](https://avatars.githubusercontent.com/u/267018309?s=64&v=4) ](https://github.com/Alix-007)
  * [ ![@bobBot-claw](https://avatars.githubusercontent.com/u/268404736?s=64&v=4) ](https://github.com/bobBot-claw)
  * [ ![@nexrin](https://avatars.githubusercontent.com/u/268879349?s=64&v=4) ](https://github.com/nexrin)
  * [ ![@oliviareid-svg](https://avatars.githubusercontent.com/u/269669958?s=64&v=4) ](https://github.com/oliviareid-svg)

vincentkoc, steipete, and 116 other contributors
Assets 3
Loading
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
👍 21 birdofprey, nhmpk824-gif, RLR64, liushuangls, Haverlun, lin72h, nek1987, afgs10, IthaiT, mesutde, and 11 more reacted with thumbs up emoji 🎉 15 jokedul, obviyus, birdofprey, RentMyNick, RLR64, Yiozolm, lin72h, aswindh, zhangMINGkeq1, aviyashchin, and 5 more reacted with hooray emoji ❤️ 8 birdofprey, RLR64, lin72h, NoobPeople418, AsaadAbbas, aviyashchin, euclidesdry-tripee, and qiang1234zhang reacted with heart emoji 🚀 13 andresantonioriveros, birdofprey, hroost, kumawashere1, Anboias, RLR64, lin72h, artfaal, robinbeier, LouisCourcier, and 3 more reacted with rocket emoji 👀 3 mirraphy, mrverdant13, and qiang1234zhang reacted with eyes emoji
All reactions
  * 👍 21 reactions
  * 🎉 15 reactions
  * ❤️ 8 reactions
  * 🚀 13 reactions
  * 👀 3 reactions

41 people reacted
## openclaw 2026.3.13
14 Mar 18:04
![@onutc](https://avatars.githubusercontent.com/u/152018508?s=40&v=4) [onutc](https://github.com/onutc)
Immutable release. Only release title and notes can be modified.
[ v2026.3.13-1  ](https://github.com/openclaw/openclaw/tree/v2026.3.13-1)
This tag was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/152018508?s=64&v=4) ](https://github.com/onutc) [onutc](https://github.com/onutc) Onur
GPG key ID: 431CDA6015C0F023
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
[ `61d171a`](https://github.com/openclaw/openclaw/commit/61d171ab0b2fe4abc9afe89c518586274b4b76c2)
This commit was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
Compare
#  Choose a tag to compare
## Sorry, something went wrong.
Filter
Loading
## Sorry, something went wrong.
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
## No results found
[View all tags](https://github.com/openclaw/openclaw/tags)
[openclaw 2026.3.13](https://github.com/openclaw/openclaw/releases/tag/v2026.3.13-1)
This recovery release uses `v2026.3.13-1` because GitHub immutable releases do not allow reusing `v2026.3.13` after publication.
Important:
  * This release exists to recover the broken `v2026.3.13` tag/release path.
  * The corresponding npm version is still `2026.3.13`, not `2026.3.13-1`.
  * The `-1` suffix is for the Git tag and GitHub Release only.

## What's Changed
  * fix(compaction): use full-session token count for post-compaction sanity check by [@efe-arv](https://github.com/efe-arv) in [#28347](https://github.com/openclaw/openclaw/pull/28347)
  * fix(telegram): thread media transport policy into SSRF by [@obviyus](https://github.com/obviyus) in [#44639](https://github.com/openclaw/openclaw/pull/44639)
  * fix: handle Discord gateway metadata fetch failures by [@jalehman](https://github.com/jalehman) in [#44397](https://github.com/openclaw/openclaw/pull/44397)
  * docs: move post-release changelog entries to Unreleased by [@jalehman](https://github.com/jalehman) in [#44691](https://github.com/openclaw/openclaw/pull/44691)
  * fix(session): preserve `lastAccountId ` and `lastThreadId` on session reset by [@Lanfei](https://github.com/Lanfei) in [#44773](https://github.com/openclaw/openclaw/pull/44773)
  * Updated default model from openai-codex/gpt-5.3-codex to openai-codex/gpt-5.4 in tests. by [@jrrcdev](https://github.com/jrrcdev) in [#44367](https://github.com/openclaw/openclaw/pull/44367)
  * fix: address delivery dedupe review follow-ups by [@frankekn](https://github.com/frankekn) in [#44666](https://github.com/openclaw/openclaw/pull/44666)
  * CLI: align xhigh thinking help text by [@frankekn](https://github.com/frankekn) in [#44819](https://github.com/openclaw/openclaw/pull/44819)
  * docs: fix changelog credit for xhigh help by [@frankekn](https://github.com/frankekn) in [#44874](https://github.com/openclaw/openclaw/pull/44874)
  * fix(agents): drop Anthropic thinking blocks on replay by [@frankekn](https://github.com/frankekn) in [#44843](https://github.com/openclaw/openclaw/pull/44843)
  * docs: fix session key :dm: → :direct: by [@Lanfei](https://github.com/Lanfei) in [#26506](https://github.com/openclaw/openclaw/pull/26506)
  * feat(android): redesign chat settings UI by [@obviyus](https://github.com/obviyus) in [#44894](https://github.com/openclaw/openclaw/pull/44894)
  * fix(agents): avoid injecting memory file twice on case-insensitive mounts by [@Lanfei](https://github.com/Lanfei) in [#26054](https://github.com/openclaw/openclaw/pull/26054)
  * Docker: add OPENCLAW_TZ timezone support by [@Lanfei](https://github.com/Lanfei) in [#34119](https://github.com/openclaw/openclaw/pull/34119)
  * Android: fix HttpURLConnection leak in TalkModeVoiceResolver by [@Kaneki-x](https://github.com/Kaneki-x) in [#43780](https://github.com/openclaw/openclaw/pull/43780)
  * fix(agents): respect explicit user compat overrides for non-native openai-completions by [@cheapestinference](https://github.com/cheapestinference) in [#44432](https://github.com/openclaw/openclaw/pull/44432)
  * test(config): cover requiresOpenAiAnthropicToolPayload in compat schema fixture by [@xingsy97](https://github.com/xingsy97) in [#43438](https://github.com/openclaw/openclaw/pull/43438)
  * fix(agents): rephrase session reset prompt to avoid Azure content filter by [@xingsy97](https://github.com/xingsy97) in [#43403](https://github.com/openclaw/openclaw/pull/43403)
  * fix(config): add missing params field to agents.list[] validation schema by [@atian8179](https://github.com/atian8179) in [#41171](https://github.com/openclaw/openclaw/pull/41171)
  * fix(android): use Google Code Scanner for onboarding QR by [@obviyus](https://github.com/obviyus) in [#45021](https://github.com/openclaw/openclaw/pull/45021)
  * fix: restore web fetch firecrawl config in runtime zod schema by [@stim64045-spec](https://github.com/stim64045-spec) in [#42583](https://github.com/openclaw/openclaw/pull/42583)
  * fix(signal): add groups config to Signal channel schema by [@unisone](https://github.com/unisone) in [#27199](https://github.com/openclaw/openclaw/pull/27199)
  * feat(ios): add onboarding welcome pager by [@ngutman](https://github.com/ngutman) in [#45054](https://github.com/openclaw/openclaw/pull/45054)
  * small addition to .gitignore by @Sovtoshi-SC in [#42879](https://github.com/openclaw/openclaw/pull/42879)
  * fix(discovery): add missing domain to wideArea Zod config schema by [@ingyukoh](https://github.com/ingyukoh) in [#35615](https://github.com/openclaw/openclaw/pull/35615)
  * fix(ui): keep shared auth on insecure control-ui connects by [@velvet-shark](https://github.com/velvet-shark) in [#45088](https://github.com/openclaw/openclaw/pull/45088)
  * fix: preserve persona and language continuity in compaction summaries by [@keepitmello](https://github.com/keepitmello) in [#10456](https://github.com/openclaw/openclaw/pull/10456)
  * ui: mobile navigation drawer & theme variant refinements by [@BunsDev](https://github.com/BunsDev) in [#45107](https://github.com/openclaw/openclaw/pull/45107)
  * fix: resolve target agent workspace for cross-agent subagent spawns by [@moshehbenavraham](https://github.com/moshehbenavraham) in [#40176](https://github.com/openclaw/openclaw/pull/40176)
  * fix(ollama): hide native reasoning-only output by [@frankekn](https://github.com/frankekn) in [#45330](https://github.com/openclaw/openclaw/pull/45330)
  * test: annotate chat abort helper exports by [@frankekn](https://github.com/frankekn) in [#45346](https://github.com/openclaw/openclaw/pull/45346)
  * Fix incorrect rendering of brave costs in docs by [@keelanfh](https://github.com/keelanfh) in [#44989](https://github.com/openclaw/openclaw/pull/44989)
  * security(docker): prevent gateway token leak in Docker build context by [@xingsy97](https://github.com/xingsy97) in [#44956](https://github.com/openclaw/openclaw/pull/44956)
  * refactor: remove redundant ?? undefined in Slack probe by [@Cafexss](https://github.com/Cafexss) in [#44775](https://github.com/openclaw/openclaw/pull/44775)
  * fix(ui): restore chat-new-messages class on scroll pill button by [@Astro-Han](https://github.com/Astro-Han) in [#44856](https://github.com/openclaw/openclaw/pull/44856)
  * fix(windows): suppress visible console windows during restart and process cleanup by [@MoerAI](https://github.com/MoerAI) in [#44842](https://github.com/openclaw/openclaw/pull/44842)
  * Slack: add opt-in interactive reply directives by [@vincentkoc](https://github.com/vincentkoc) in [#44607](https://github.com/openclaw/openclaw/pull/44607)
  * Docs: describe Slack interactive replies by [@vincentkoc](https://github.com/vincentkoc) in [#45463](https://github.com/openclaw/openclaw/pull/45463)
  * fix(cron): prevent isolated cron nested lane deadlocks by [@vincentkoc](https://github.com/vincentkoc) in [#45459](https://github.com/openclaw/openclaw/pull/45459)
  * Fix updater refresh cwd for service reinstall by [@vincentkoc](https://github.com/vincentkoc) in [#45452](https://github.com/openclaw/openclaw/pull/45452)
  * [codex] Polish sidebar status, agent skills, and chat rendering by [@BunsDev](https://github.com/BunsDev) in [#45451](https://github.com/openclaw/openclaw/pull/45451)
  * perf(build): deduplicate plugin-sdk chunks to fix ~2x memory regression by [@TarasShyn](https://github.com/TarasShyn) in [#45426](https://github.com/openclaw/openclaw/pull/45426)
  * Guard updater service refresh against missing invocation cwd by [@vincentkoc](https://github.com/vincentkoc) in [#45486](https://github.com/openclaw/openclaw/pull/45486)
  * fix(browser): normalize batch act dispatch for selector and batch support by [@vincentkoc](https://github.com/vincentkoc) in [#45457](https://github.com/openclaw/openclaw/pull/45457)
  * docs(android): note that app is not publicly released yet by [@eengad](https://github.com/eengad) in [#23051](https://github.com/openclaw/openclaw/pull/23051)
  * fix(browser): follow up batch failure and limit handling by [@vincentkoc](https://github.com/vincentkoc) in [#45506](https://github.com/openclaw/openclaw/pull/45506)
  * docker: add apt-get upgrade to all Dockerfiles by [@jacobtomlinson](https://github.com/jacobtomlinson) in [#45384](https://github.com/openclaw/openclaw/pull/45384)
  * fix(config): avoid Anthropic startup crash by [@BunsDev](https://github.com/BunsDev) in [#45520](https://github.com/openclaw/openclaw/pull/45520)
  * test: preserve wrapper behavior for targeted runs by [@Takhoffman](https://github.com/Takhoffman) in [#45518](https://github.com/openclaw/openclaw/pull/45518)
  * UI: fix chat context notice icon sizing by [@BunsDev](https://github.com/BunsDev) in [#45533](https://github.com/openclaw/openclaw/pull/45533)
  * fix(ui): stop dashboard chat history reload storm by [@BunsDev](https://github.com/BunsDev) in [#45541](https://github.com/openclaw/openclaw/pull/45541)
  * fix: retry Telegram inbound media downloads over IPv4 fallback by [@frankekn](https://github.com/frankekn) in [#45327](https://github.com/openclaw/openclaw/pull/45327)
  * fix(feishu): preserve non-ASCII filenames in file uploads ([#33912](https://github.com/openclaw/openclaw/issues/33912)) by [@fabiaodemianyang](https://github.com/fabiaodemianyang) in [#34262](https://github.com/openclaw/openclaw/pull/34262)
  * macOS: respect exec-approvals.json settings in gateway prompter by [@sliekens](https://github.com/sliekens) in [#13707](https://github.com/openclaw/openclaw/pull/13707)
  * fix(ui): keep oversized chat replies readable by [@BunsDev](https://github.com/BunsDev) in [#45559](https://github.com/openclaw/openclaw/pull/45559)
  * fix(gateway/ui): restore control-ui auth bypass and classify connect failures by [@sallyom](https://github.com/sallyom) in [#45512](https://github.com/openclaw/openclaw/pull/45512)
  * fix(macos): prevent PortGuard from killing Docker Desktop in remote mode by [@teslamint](https://github.com/teslamint) in [#13798](https://github.com/openclaw/openclaw/pull/13798)
  * fix(sessions): create transcript file on chat.inject when missing by [@2233admin](https://github.com/2233admin) in [#36645](https://github.com/openclaw/openclaw/pull/36645)
  * Plugins: fail fast on channel and binding collisions by [@vincentkoc](https://github.com/vincentkoc) in [#45628](https://github.com/openclaw/openclaw/pull/45628)
  * fix(macos): align minimum Node.js version with runtime guard (22.16.0) by [@ImLukeF](https://github.com/ImLukeF) in [#45640](https://github.com/openclaw/openclaw/pull/45640)
  * fix(agents): preserve blank local custom-provider API keys after onboarding by [@frankekn](https://github.com/frankekn) in [#45631](https://github.com/openclaw/openclaw/pull/45631)
  * fix(browser): harden existing-session driver validation and session lifecycle by [@odysseus0](https://github.com/odysseus0) in [#45682](https://github.com/openclaw/openclaw/pull/45682)
  * fix(feishu): add early event-level dedup to prevent duplicate replies by [@yunweibang](https://github.com/yunweibang) in [#43762](https://github.com/openclaw/openclaw/pull/43762)
  * fix(models): apply Gemini model-id normalization to google-vertex provider by [@scoootscooob](https://github.com/scoootscooob) in [#42435](https://github.com/openclaw/openclaw/pull/42435)
  * Gateway: treat scope-limited probe RPC as degraded reachability by [@joshavant](https://github.com/joshavant) in [#45622](https://github.com/openclaw/openclaw/pull/45622)
  * fix(gateway): bound unanswered client requests by [@Takhoffman](https://github.com/Takhoffman) in [#45689](https://github.com/openclaw/openclaw/pull/45689)

## New Contributors
  * [@jrrcdev](https://github.com/jrrcdev) made their first contribution in [#44367](https://github.com/openclaw/openclaw/pull/44367)
  * [@Kaneki-x](https://github.com/Kaneki-x) made their first contribution in [#43780](https://github.com/openclaw/openclaw/pull/43780)
  * [@cheapestinference](https://github.com/cheapestinference) made their first contribution in [#44432](https://github.com/openclaw/openclaw/pull/44432)
  * [@xingsy97](https://github.com/xingsy97) made their first contribution in [#43438](https://github.com/openclaw/openclaw/pull/43438)
  * [@atian8179](https://github.com/atian8179) made their first contribution in [#41171](https://github.com/openclaw/openclaw/pull/41171)
  * [@stim64045-spec](https://github.com/stim64045-spec) made their first contribution in [#42583](https://github.com/openclaw/openclaw/pull/42583)
  * @Sovtoshi-SC made their first contribution in [#42879](https://github.com/openclaw/openclaw/pull/42879)
  * [@keepitmello](https://github.com/keepitmello) made their first contribution in [#10456](https://github.com/openclaw/openclaw/pull/10456)
  * [@moshehbenavraham](https://github.com/moshehbenavraham) made their first contribution in [#40176](https://github.com/openclaw/openclaw/pull/40176)
  * [@keelanfh](https://github.com/keelanfh) made their first contribution in [#44989](https://github.com/openclaw/openclaw/pull/44989)
  * [@Cafexss](https://github.com/Cafexss) made their first contribution in [#44775](https://github.com/openclaw/openclaw/pull/44775)
  * [@Astro-Han](https://github.com/Astro-Han) made their first contribution in [#44856](https://github.com/openclaw/openclaw/pull/44856)
  * [@eengad](https://github.com/eengad) made their first contribution in https:...

[Read more](https://github.com/openclaw/openclaw/releases/tag/v2026.3.13-1)
### Contributors
  * [ ![@vincentkoc](https://avatars.githubusercontent.com/u/25068?s=64&v=4) ](https://github.com/vincentkoc)
  * [ ![@velvet-shark](https://avatars.githubusercontent.com/u/126378?s=64&v=4) ](https://github.com/velvet-shark)
  * [ ![@teslamint](https://avatars.githubusercontent.com/u/158752?s=64&v=4) ](https://github.com/teslamint)
  * [ ![@jalehman](https://avatars.githubusercontent.com/u/550978?s=64&v=4) ](https://github.com/jalehman)
  * [ ![@Takhoffman](https://avatars.githubusercontent.com/u/781889?s=64&v=4) ](https://github.com/Takhoffman)
  * [ ![@joshavant](https://avatars.githubusercontent.com/u/830519?s=64&v=4) ](https://github.com/joshavant)
  * [ ![@ngutman](https://avatars.githubusercontent.com/u/1540134?s=64&v=4) ](https://github.com/ngutman)
  * [ ![@sliekens](https://avatars.githubusercontent.com/u/1583241?s=64&v=4) ](https://github.com/sliekens)
  * [ ![@jacobtomlinson](https://avatars.githubusercontent.com/u/1610850?s=64&v=4) ](https://github.com/jacobtomlinson)
  * [ ![@Lanfei](https://avatars.githubusercontent.com/u/2156642?s=64&v=4) ](https://github.com/Lanfei)
  * [ ![@frankekn](https://avatars.githubusercontent.com/u/4488090?s=64&v=4) ](https://github.com/frankekn)
  * [ ![@yunweibang](https://avatars.githubusercontent.com/u/5226861?s=64&v=4) ](https://github.com/yunweibang)
  * [ ![@ingyukoh](https://avatars.githubusercontent.com/u/6015960?s=64&v=4) ](https://github.com/ingyukoh)
  * [ ![@Kaneki-x](https://avatars.githubusercontent.com/u/6857108?s=64&v=4) ](https://github.com/Kaneki-x)
  * [ ![@odysseus0](https://avatars.githubusercontent.com/u/8635094?s=64&v=4) ](https://github.com/odysseus0)
  * [ ![@sallyom](https://avatars.githubusercontent.com/u/11166065?s=64&v=4) ](https://github.com/sallyom)
  * [ ![@Cafexss](https://avatars.githubusercontent.com/u/13113185?s=64&v=4) ](https://github.com/Cafexss)
  * [ ![@moshehbenavraham](https://avatars.githubusercontent.com/u/17122072?s=64&v=4) ](https://github.com/moshehbenavraham)
  * [ ![@jrrcdev](https://avatars.githubusercontent.com/u/19454127?s=64&v=4) ](https://github.com/jrrcdev)
  * [ ![@keelanfh](https://avatars.githubusercontent.com/u/19519457?s=64&v=4) ](https://github.com/keelanfh)
  * [ ![@obviyus](https://avatars.githubusercontent.com/u/22031114?s=64&v=4) ](https://github.com/obviyus)
  * [ ![@MoerAI](https://avatars.githubusercontent.com/u/26067127?s=64&v=4) ](https://github.com/MoerAI)
  * [ ![@unisone](https://avatars.githubusercontent.com/u/32521398?s=64&v=4) ](https://github.com/unisone)
  * [ ![@eengad](https://avatars.githubusercontent.com/u/36604865?s=64&v=4) ](https://github.com/eengad)
  * [ ![@2233admin](https://avatars.githubusercontent.com/u/57929895?s=64&v=4) ](https://github.com/2233admin)
  * [ ![@TarasShyn](https://avatars.githubusercontent.com/u/67313527?s=64&v=4) ](https://github.com/TarasShyn)
  * [ ![@BunsDev](https://avatars.githubusercontent.com/u/68980965?s=64&v=4) ](https://github.com/BunsDev)
  * [ ![@keepitmello](https://avatars.githubusercontent.com/u/71975659?s=64&v=4) ](https://github.com/keepitmello)
  * [ ![@xingsy97](https://avatars.githubusercontent.com/u/87063252?s=64&v=4) ](https://github.com/xingsy97)
  * [ ![@ImLukeF](https://avatars.githubusercontent.com/u/92253590?s=64&v=4) ](https://github.com/ImLukeF)
  * [ ![@scoootscooob](https://avatars.githubusercontent.com/u/167050519?s=64&v=4) ](https://github.com/scoootscooob)
  * [ ![@fabiaodemianyang](https://avatars.githubusercontent.com/u/221485585?s=64&v=4) ](https://github.com/fabiaodemianyang)
  * [ ![@cheapestinference](https://avatars.githubusercontent.com/u/239757197?s=64&v=4) ](https://github.com/cheapestinference)
  * [ ![@Astro-Han](https://avatars.githubusercontent.com/u/255364436?s=64&v=4) ](https://github.com/Astro-Han)
  * [ ![@atian8179](https://avatars.githubusercontent.com/u/255488364?s=64&v=4) ](https://github.com/atian8179)
  * [ ![@stim64045-spec](https://avatars.githubusercontent.com/u/259352523?s=64&v=4) ](https://github.com/stim64045-spec)
  * [ ![@efe-arv](https://avatars.githubusercontent.com/u/259833796?s=64&v=4) ](https://github.com/efe-arv)

vincentkoc, velvet-shark, and 35 other contributors
Assets 3
Loading
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
👍 241 lassestilvang, kasnol, RLR64, digitalshah314, LostBeard, zeroonedev1, vst93, mesutde, EthanThePhoenix38, orielhaim, and 231 more reacted with thumbs up emoji 😄 26 tinwonda, kong62, lin72h, haiyang6, ntsc000, classronin, MalavyaRaval, davidtost5, 261237407, birdofprey, and 16 more reacted with laugh emoji 🎉 27 kong62, pixel-miner, lin72h, i-iooi-i, XiaoYee, ntsc000, MalavyaRaval, 261237407, birdofprey, chib30333, and 17 more reacted with hooray emoji ❤️ 34 kong62, lin72h, nakheel77, John-Codes, i-iooi-i, Endogen, ntsc000, zumermalik, MalavyaRaval, 261237407, and 24 more reacted with heart emoji 🚀 27 StudentWeis, mrverdant13, kong62, egoan82, NobleWilson, lin72h, i-iooi-i, Mushy-Snugglebites-badonkadonk, chengjiangyue, Endogen, and 17 more reacted with rocket emoji 👀 17 kong62, gxmq, RamessesN, ntsc000, MalavyaRaval, 261237407, birdofprey, 1186258278, zfh521, laterandlater, and 7 more reacted with eyes emoji
All reactions
  * 👍 241 reactions
  * 😄 26 reactions
  * 🎉 27 reactions
  * ❤️ 34 reactions
  * 🚀 27 reactions
  * 👀 17 reactions

284 people reacted
## openclaw 2026.3.13-beta.1
14 Mar 05:17
![@steipete](https://avatars.githubusercontent.com/u/58493?s=40&v=4) [steipete](https://github.com/steipete)
Immutable release. Only release title and notes can be modified.
[ v2026.3.13-beta.1  ](https://github.com/openclaw/openclaw/tree/v2026.3.13-beta.1)
This tag was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
[ `94a2926`](https://github.com/openclaw/openclaw/commit/94a292686cb41ea5452f71663fabc48231452a97)
This commit was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
Compare
#  Choose a tag to compare
## Sorry, something went wrong.
Filter
Loading
## Sorry, something went wrong.
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
## No results found
[View all tags](https://github.com/openclaw/openclaw/tags)
[openclaw 2026.3.13-beta.1](https://github.com/openclaw/openclaw/releases/tag/v2026.3.13-beta.1) Pre-release
Pre-release
Pre-release for npm beta tag `v2026.3.13-beta.1`.
macOS assets are built with stable app version `2026.3.13` so they can be reused for the later non-beta release. `appcast.xml` is intentionally unchanged in this pre-release.
### Changes
  * Android/chat settings: redesign the chat settings sheet with grouped device and media sections, refresh the Connect and Voice tabs, and tighten the chat composer/session header for a denser mobile layout. ([#44894](https://github.com/openclaw/openclaw/pull/44894)) Thanks [@obviyus](https://github.com/obviyus).
  * iOS/onboarding: add a first-run welcome pager before gateway setup, stop auto-opening the QR scanner, and show `/pair qr` instructions on the connect step. ([#45054](https://github.com/openclaw/openclaw/pull/45054)) Thanks [@ngutman](https://github.com/ngutman).
  * Browser/existing-session: add an official Chrome DevTools MCP attach mode for signed-in live Chrome sessions, with docs for `chrome://inspect/#remote-debugging` enablement and direct backlinks to Chrome’s own setup guides.
  * Browser/agents: add built-in `profile="user"` for the logged-in host browser and `profile="chrome-relay"` for the extension relay, so agent browser calls can prefer the real signed-in browser without the extra `browserSession` selector.
  * Browser/act automation: add batched actions, selector targeting, and delayed clicks for browser act requests with normalized batch dispatch. Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Docker/timezone override: add `OPENCLAW_TZ` so `docker-setup.sh` can pin gateway and CLI containers to a chosen IANA timezone instead of inheriting the daemon default. ([#34119](https://github.com/openclaw/openclaw/pull/34119)) Thanks [@Lanfei](https://github.com/Lanfei).
  * Dependencies/pi: bump `@mariozechner/pi-agent-core`, `@mariozechner/pi-ai`, `@mariozechner/pi-coding-agent`, and `@mariozechner/pi-tui` to `0.58.0`.

### Fixes
  * Dashboard/chat UI: stop reloading full chat history on every live tool result in dashboard v2 so tool-heavy runs no longer trigger UI freeze/re-render storms while the final event still refreshes persisted history. ([#45541](https://github.com/openclaw/openclaw/pull/45541)) Thanks [@BunsDev](https://github.com/BunsDev).
  * Ollama/reasoning visibility: stop promoting native `thinking` and `reasoning` fields into final assistant text so local reasoning models no longer leak internal thoughts in normal replies. ([#45330](https://github.com/openclaw/openclaw/pull/45330)) Thanks [@xi7ang](https://github.com/xi7ang).
  * Android/onboarding QR scan: switch setup QR scanning to Google Code Scanner so onboarding uses a more reliable scanner instead of the legacy embedded ZXing flow. ([#45021](https://github.com/openclaw/openclaw/pull/45021)) Thanks [@obviyus](https://github.com/obviyus).
  * Browser/existing-session: harden driver validation and session lifecycle so transport errors trigger reconnects while tool-level errors preserve the session, and extract shared ARIA role sets to deduplicate Playwright and Chrome MCP snapshot paths. ([#45682](https://github.com/openclaw/openclaw/pull/45682)) Thanks [@odysseus0](https://github.com/odysseus0).
  * Browser/existing-session: accept text-only `list_pages` and `new_page` responses from Chrome DevTools MCP so live-session tab discovery and new-tab open flows keep working when the server omits structured page metadata.
  * Control UI/insecure auth: preserve explicit shared token and password auth on plain-HTTP Control UI connects so LAN and reverse-proxy sessions no longer drop shared auth before the first WebSocket handshake. ([#45088](https://github.com/openclaw/openclaw/pull/45088)) Thanks [@velvet-shark](https://github.com/velvet-shark).
  * Gateway/session reset: preserve `lastAccountId` and `lastThreadId` across gateway session resets so replies keep routing back to the same account and thread after `/reset`. ([#44773](https://github.com/openclaw/openclaw/pull/44773)) Thanks [@Lanfei](https://github.com/Lanfei).
  * macOS/onboarding: avoid self-restarting freshly bootstrapped launchd gateways and give new daemon installs longer to become healthy, so `openclaw onboard --install-daemon` no longer false-fails on slower Macs and fresh VM snapshots.
  * Gateway/status: add `openclaw gateway status --require-rpc` and clearer Linux non-interactive daemon-install failure reporting so automation can fail hard on probe misses instead of treating a printed RPC error as green.
  * macOS/exec approvals: respect per-agent exec approval settings in the gateway prompter, including allowlist fallback when the native prompt cannot be shown, so gateway-triggered `system.run` requests follow configured policy instead of always prompting or denying unexpectedly. ([#13707](https://github.com/openclaw/openclaw/pull/13707)) Thanks [@sliekens](https://github.com/sliekens).
  * Telegram/media downloads: thread the same direct or proxy transport policy into SSRF-guarded file fetches so inbound attachments keep working when Telegram falls back between env-proxy and direct networking. ([#44639](https://github.com/openclaw/openclaw/pull/44639)) Thanks [@obviyus](https://github.com/obviyus).
  * Telegram/inbound media IPv4 fallback: retry SSRF-guarded Telegram file downloads once with the same IPv4 fallback policy as Bot API calls so fresh installs on IPv6-broken hosts no longer fail to download inbound images.
  * Windows/gateway install: bound `schtasks` calls and fall back to the Startup-folder login item when task creation hangs, so native `openclaw gateway install` fails fast instead of wedging forever on broken Scheduled Task setups.
  * Windows/gateway stop: resolve Startup-folder fallback listeners from the installed `gateway.cmd` port, so `openclaw gateway stop` now actually kills fallback-launched gateway processes before restart.
  * Windows/gateway status: reuse the installed service command environment when reading runtime status, so startup-fallback gateways keep reporting the configured port and running state in `gateway status --json` instead of falling back to `gateway port unknown`.
  * Windows/gateway auth: stop attaching device identity on local loopback shared-token and password gateway calls, so native Windows agent replies no longer log stale `device signature expired` fallback noise before succeeding.
  * Discord/gateway startup: treat plain-text and transient `/gateway/bot` metadata fetch failures as transient startup errors so Discord gateway boot no longer crashes on unhandled rejections. ([#44397](https://github.com/openclaw/openclaw/pull/44397)) Thanks [@jalehman](https://github.com/jalehman).
  * Slack/probe: keep `auth.test()` bot and team metadata mapping stable while simplifying the probe result path. ([#44775](https://github.com/openclaw/openclaw/pull/44775)) Thanks [@Cafexss](https://github.com/Cafexss).
  * Dashboard/chat UI: render oversized plain-text replies as normal paragraphs instead of capped gray code blocks, so long desktop chat responses stay readable without tab-switching refreshes.
  * Dashboard/chat UI: restore the `chat-new-messages` class on the New messages scroll pill so the button uses its existing compact styling instead of rendering as a full-screen SVG overlay. ([#44856](https://github.com/openclaw/openclaw/pull/44856)) Thanks [@Astro-Han](https://github.com/Astro-Han).
  * Gateway/Control UI: restore the operator-only device-auth bypass and classify browser connect failures so origin and device-identity problems no longer show up as auth errors in the Control UI and web chat. ([#45512](https://github.com/openclaw/openclaw/pull/45512)) thanks [@sallyom](https://github.com/sallyom).
  * macOS/voice wake: stop crashing wake-word command extraction when speech segment ranges come from a different transcript instance.
  * Discord/allowlists: honor raw `guild_id` when hydrated guild objects are missing so allowlisted channels and threads like `#maintainers` no longer get false-dropped before channel allowlist checks.
  * macOS/runtime locator: require Node >=22.16.0 during macOS runtime discovery so the app no longer accepts Node versions that the main runtime guard rejects later. Thanks [@sumleo](https://github.com/sumleo).
  * Agents/custom providers: preserve blank API keys for loopback OpenAI-compatible custom providers by clearing the synthetic Authorization header at runtime, while keeping explicit apiKey and oauth/token config from silently downgrading into fake bearer auth. ([#45631](https://github.com/openclaw/openclaw/pull/45631)) Thanks [@xinhuagu](https://github.com/xinhuagu).
  * Models/google-vertex Gemini flash-lite normalization: apply existing bare-ID preview normalization to `google-vertex` model refs and provider configs so `google-vertex/gemini-3.1-flash-lite` resolves as `gemini-3.1-flash-lite-preview`. ([#42435](https://github.com/openclaw/openclaw/pull/42435)) thanks [@scoootscooob](https://github.com/scoootscooob).
  * iMessage/remote attachments: reject unsafe remote attachment paths before spawning SCP, so sender-controlled filenames can no longer inject shell metacharacters into remote media staging. Thanks [@lintsinghua](https://github.com/lintsinghua).
  * Telegram/webhook auth: validate the Telegram webhook secret before reading or parsing request bodies, so unauthenticated requests are rejected immediately instead of consuming up to 1 MB first. Thanks [@space08](https://github.com/space08).
  * Security/device pairing: make bootstrap setup codes single-use so pending device pairing requests cannot be silently replayed and widened to admin before approval. Thanks [@tdjackey](https://github.com/tdjackey).
  * Security/external content: strip zero-width and soft-hyphen marker-splitting characters during boundary sanitization so spoofed `EXTERNAL_UNTRUSTED_CONTENT` markers fall back to the existing hardening path instead of bypassing marker normalization.
  * Security/exec approvals: unwrap more `pnpm` runtime forms during approval binding, including `pnpm --reporter ... exec` and direct `pnpm node` file runs, with matching regression coverage and docs updates.
  * Security/exec approvals: fail closed for Perl `-M` and `-I` approval flows so preload and load-path module resolution stays outside approval-backed runtime execution unless the operator uses a broader explicit trust path.
  * Security/exec approvals: recognize PowerShell `-File` and `-f` wrapper forms during inline-command extraction so approval and command-analysis paths treat file-based PowerShell launches like the existing `-Command` variants.
  * Security/exec approvals: unwrap `env` dispatch wrappers inside shell-segment allowlist resolution on macOS so `env FOO=bar /path/to/bin` resolves against the effective executable instead of the wrapper token.
  * Security/exec approvals: treat backslash-newline as shell line continuation during macOS shell-chain parsing so line-continued `$(` substitutions fail closed instead of slipping past command-substitution checks.
  * Security/exec approvals: bind macOS skill auto-allow trust to both executable name and resolved path so same-basename binaries no longer inherit trust from unrelated skill bins.
  * Build/plugin-sdk bundling: bundle plugin-sdk subpath entries in one shared build pass so published packages stop duplicating shared chunks and avoid the recent plugin-sdk memory blow-up. ([#45426](https://github.com/openclaw/openclaw/pull/45426)) Thanks [@TarasShyn](https://github.com/TarasShyn).
  * Cron/isolated sessions: route nested cron-triggered embedded runner work onto the nested lane so isolated cron jobs no longer deadlock when compaction or other queued inner work runs. Thanks [@vincentkoc](https://github.com/vincentkoc)...

[Read more](https://github.com/openclaw/openclaw/releases/tag/v2026.3.13-beta.1)
### Contributors
  * [ ![@vincentkoc](https://avatars.githubusercontent.com/u/25068?s=64&v=4) ](https://github.com/vincentkoc)
  * [ ![@velvet-shark](https://avatars.githubusercontent.com/u/126378?s=64&v=4) ](https://github.com/velvet-shark)
  * [ ![@jalehman](https://avatars.githubusercontent.com/u/550978?s=64&v=4) ](https://github.com/jalehman)
  * [ ![@xinhuagu](https://avatars.githubusercontent.com/u/562450?s=64&v=4) ](https://github.com/xinhuagu)
  * [ ![@ngutman](https://avatars.githubusercontent.com/u/1540134?s=64&v=4) ](https://github.com/ngutman)
  * [ ![@sliekens](https://avatars.githubusercontent.com/u/1583241?s=64&v=4) ](https://github.com/sliekens)
  * [ ![@Lanfei](https://avatars.githubusercontent.com/u/2156642?s=64&v=4) ](https://github.com/Lanfei)
  * [ ![@ingyukoh](https://avatars.githubusercontent.com/u/6015960?s=64&v=4) ](https://github.com/ingyukoh)
  * [ ![@tdjackey](https://avatars.githubusercontent.com/u/6791132?s=64&v=4) ](https://github.com/tdjackey)
  * [ ![@odysseus0](https://avatars.githubusercontent.com/u/8635094?s=64&v=4) ](https://github.com/odysseus0)
  * [ ![@sallyom](https://avatars.githubusercontent.com/u/11166065?s=64&v=4) ](https://github.com/sallyom)
  * [ ![@Cafexss](https://avatars.githubusercontent.com/u/13113185?s=64&v=4) ](https://github.com/Cafexss)
  * [ ![@space08](https://avatars.githubusercontent.com/u/21030542?s=64&v=4) ](https://github.com/space08)
  * [ ![@obviyus](https://avatars.githubusercontent.com/u/22031114?s=64&v=4) ](https://github.com/obviyus)
  * [ ![@sumleo](https://avatars.githubusercontent.com/u/29517764?s=64&v=4) ](https://github.com/sumleo)
  * [ ![@unisone](https://avatars.githubusercontent.com/u/32521398?s=64&v=4) ](https://github.com/unisone)
  * [ ![@TarasShyn](https://avatars.githubusercontent.com/u/67313527?s=64&v=4) ](https://github.com/TarasShyn)
  * [ ![@BunsDev](https://avatars.githubusercontent.com/u/68980965?s=64&v=4) ](https://github.com/BunsDev)
  * [ ![@keepitmello](https://avatars.githubusercontent.com/u/71975659?s=64&v=4) ](https://github.com/keepitmello)
  * [ ![@xingsy97](https://avatars.githubusercontent.com/u/87063252?s=64&v=4) ](https://github.com/xingsy97)
  * [ ![@lintsinghua](https://avatars.githubusercontent.com/u/129816813?s=64&v=4) ](https://github.com/lintsinghua)
  * [ ![@scoootscooob](https://avatars.githubusercontent.com/u/167050519?s=64&v=4) ](https://github.com/scoootscooob)
  * [ ![@cheapestinference](https://avatars.githubusercontent.com/u/239757197?s=64&v=4) ](https://github.com/cheapestinference)
  * [ ![@Astro-Han](https://avatars.githubusercontent.com/u/255364436?s=64&v=4) ](https://github.com/Astro-Han)
  * [ ![@atian8179](https://avatars.githubusercontent.com/u/255488364?s=64&v=4) ](https://github.com/atian8179)
  * [ ![@stim64045-spec](https://avatars.githubusercontent.com/u/259352523?s=64&v=4) ](https://github.com/stim64045-spec)
  * [ ![@efe-arv](https://avatars.githubusercontent.com/u/259833796?s=64&v=4) ](https://github.com/efe-arv)
  * [ ![@xi7ang](https://avatars.githubusercontent.com/u/266449609?s=64&v=4) ](https://github.com/xi7ang)

vincentkoc, velvet-shark, and 26 other contributors
Assets 6
Loading
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
👍 4 18579992747-alt, 584805943libo-bot, militangellen-collab, and NelsonYong reacted with thumbs up emoji ❤️ 1 SilentDraft reacted with heart emoji 👀 25 mrverdant13, nakheel77, MissedShot, techedger, 44ompatil, Apartman36, 1056829479, SuoXueHui, yasir-shahhhhh, yanking, and 15 more reacted with eyes emoji
All reactions
  * 👍 4 reactions
  * ❤️ 1 reaction
  * 👀 25 reactions

30 people reacted
## openclaw 2026.3.12
13 Mar 04:26
![@steipete](https://avatars.githubusercontent.com/u/58493?s=40&v=4) [steipete](https://github.com/steipete)
Immutable release. Only release title and notes can be modified.
[ v2026.3.12  ](https://github.com/openclaw/openclaw/tree/v2026.3.12)
This tag was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
[ `70d7a08`](https://github.com/openclaw/openclaw/commit/70d7a0854c54c489eaefd56bb406ad885f2b3ea2)
This commit was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
Compare
#  Choose a tag to compare
## Sorry, something went wrong.
Filter
Loading
## Sorry, something went wrong.
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
## No results found
[View all tags](https://github.com/openclaw/openclaw/tags)
[openclaw 2026.3.12](https://github.com/openclaw/openclaw/releases/tag/v2026.3.12)
### Changes
  * Control UI/dashboard-v2: refresh the gateway dashboard with modular overview, chat, config, agent, and session views, plus a command palette, mobile bottom tabs, and richer chat tools like slash commands, search, export, and pinned messages. ([#41503](https://github.com/openclaw/openclaw/pull/41503)) Thanks [@BunsDev](https://github.com/BunsDev).
  * OpenAI/GPT-5.4 fast mode: add configurable session-level fast toggles across `/fast`, TUI, Control UI, and ACP, with per-model config defaults and OpenAI/Codex request shaping.
  * Anthropic/Claude fast mode: map the shared `/fast` toggle and `params.fastMode` to direct Anthropic API-key `service_tier` requests, with live verification for both Anthropic and OpenAI fast-mode tiers.
  * Models/plugins: move Ollama, vLLM, and SGLang onto the provider-plugin architecture, with provider-owned onboarding, discovery, model-picker setup, and post-selection hooks so core provider wiring is more modular.
  * Docs/Kubernetes: Add a starter K8s install path with raw manifests, Kind setup, and deployment docs. Thanks [@sallyom](https://github.com/sallyom) [@dzianisv](https://github.com/dzianisv) [@egkristi](https://github.com/egkristi)
  * Agents/subagents: add `sessions_yield` so orchestrators can end the current turn immediately, skip queued tool work, and carry a hidden follow-up payload into the next session turn. ([#36537](https://github.com/openclaw/openclaw/pull/36537)) thanks [@jriff](https://github.com/jriff)
  * Slack/agent replies: support `channelData.slack.blocks` in the shared reply delivery path so agents can send Block Kit messages through standard Slack outbound delivery. ([#44592](https://github.com/openclaw/openclaw/pull/44592)) Thanks [@vincentkoc](https://github.com/vincentkoc).

### Fixes
  * Security/device pairing: switch `/pair` and `openclaw qr` setup codes to short-lived bootstrap tokens so the next release no longer embeds shared gateway credentials in chat or QR pairing payloads. Thanks [@lintsinghua](https://github.com/lintsinghua).
  * Security/plugins: disable implicit workspace plugin auto-load so cloned repositories cannot execute workspace plugin code without an explicit trust decision. (`GHSA-99qw-6mr3-36qr`)([#44174](https://github.com/openclaw/openclaw/pull/44174)) Thanks [@lintsinghua](https://github.com/lintsinghua) and [@vincentkoc](https://github.com/vincentkoc).
  * Models/Kimi Coding: send `anthropic-messages` tools in native Anthropic format again so `kimi-coding` stops degrading tool calls into XML/plain-text pseudo invocations instead of real `tool_use` blocks. ([#38669](https://github.com/openclaw/openclaw/issues/38669), [#39907](https://github.com/openclaw/openclaw/issues/39907), [#40552](https://github.com/openclaw/openclaw/issues/40552)) Thanks [@opriz](https://github.com/opriz).
  * TUI/chat log: reuse the active assistant message component for the same streaming run so `openclaw tui` no longer renders duplicate assistant replies. ([#35364](https://github.com/openclaw/openclaw/pull/35364)) Thanks [@lisitan](https://github.com/lisitan).
  * Telegram/model picker: make inline model button selections persist the chosen session model correctly, clear overrides when selecting the configured default, and include effective fallback models in `/models` button validation. ([#40105](https://github.com/openclaw/openclaw/pull/40105)) Thanks [@avirweb](https://github.com/avirweb).
  * Cron/proactive delivery: keep isolated direct cron sends out of the write-ahead resend queue so transient-send retries do not replay duplicate proactive messages after restart. ([#40646](https://github.com/openclaw/openclaw/pull/40646)) Thanks [@openperf](https://github.com/openperf) and [@vincentkoc](https://github.com/vincentkoc).
  * Models/Kimi Coding: send the built-in `User-Agent: claude-code/0.1.0` header by default for `kimi-coding` while still allowing explicit provider headers to override it, so Kimi Code subscription auth can work without a local header-injection proxy. ([#30099](https://github.com/openclaw/openclaw/issues/30099)) Thanks [@Amineelfarssi](https://github.com/Amineelfarssi) and [@vincentkoc](https://github.com/vincentkoc).
  * Models/OpenAI Codex Spark: keep `gpt-5.3-codex-spark` working on the `openai-codex/*` path via resolver fallbacks and clearer Codex-only handling, while continuing to suppress the stale direct `openai/*` Spark row that OpenAI rejects live.
  * Ollama/Kimi Cloud: apply the Moonshot Kimi payload compatibility wrapper to Ollama-hosted Kimi models like `kimi-k2.5:cloud`, so tool routing no longer breaks when thinking is enabled. ([#41519](https://github.com/openclaw/openclaw/issues/41519)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Moonshot CN API: respect explicit `baseUrl` (api.moonshot.cn) in implicit provider resolution so platform.moonshot.cn API keys authenticate correctly instead of returning HTTP 401. ([#33637](https://github.com/openclaw/openclaw/issues/33637)) Thanks [@chengzhichao-xydt](https://github.com/chengzhichao-xydt).
  * Kimi Coding/provider config: respect explicit `models.providers["kimi-coding"].baseUrl` when resolving the implicit provider so custom Kimi Coding endpoints no longer get overwritten by the built-in default. ([#36353](https://github.com/openclaw/openclaw/issues/36353)) Thanks [@2233admin](https://github.com/2233admin).
  * Gateway/main-session routing: keep TUI and other `mode:UI` main-session sends on the internal surface when `deliver` is enabled, so replies no longer inherit the session's persisted Telegram/WhatsApp route. ([#43918](https://github.com/openclaw/openclaw/pull/43918)) Thanks [@obviyus](https://github.com/obviyus).
  * BlueBubbles/self-chat echo dedupe: drop reflected duplicate webhook copies only when a matching `fromMe` event was just seen for the same chat, body, and timestamp, preventing self-chat loops without broad webhook suppression. Related to [#32166](https://github.com/openclaw/openclaw/issues/32166). ([#38442](https://github.com/openclaw/openclaw/pull/38442)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * iMessage/self-chat echo dedupe: drop reflected duplicate copies only when a matching `is_from_me` event was just seen for the same chat, text, and `created_at`, preventing self-chat loops without broad text-only suppression. Related to [#32166](https://github.com/openclaw/openclaw/issues/32166). ([#38440](https://github.com/openclaw/openclaw/pull/38440)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Subagents/completion announce retries: raise the default announce timeout to 90 seconds and stop retrying gateway-timeout failures for externally delivered completion announces, preventing duplicate user-facing completion messages after slow gateway responses. Fixes [#41235](https://github.com/openclaw/openclaw/issues/41235). Thanks [@vasujain00](https://github.com/vasujain00) and [@vincentkoc](https://github.com/vincentkoc).
  * Mattermost/block streaming: fix duplicate message delivery (one threaded, one top-level) when block streaming is active by excluding `replyToId` from the block reply dedup key and adding an explicit `threading` dock to the Mattermost plugin. ([#41362](https://github.com/openclaw/openclaw/pull/41362)) Thanks [@mathiasnagler](https://github.com/mathiasnagler) and [@vincentkoc](https://github.com/vincentkoc).
  * Mattermost/reply media delivery: pass agent-scoped `mediaLocalRoots` through shared reply delivery so allowed local files upload correctly from button, slash-command, and model-picker replies. ([#44021](https://github.com/openclaw/openclaw/pull/44021)) Thanks [@LyleLiu666](https://github.com/LyleLiu666).
  * macOS/Reminders: add the missing `NSRemindersUsageDescription` to the bundled app so `apple-reminders` can trigger the system permission prompt from OpenClaw.app. ([#8559](https://github.com/openclaw/openclaw/pull/8559)) Thanks [@dinakars777](https://github.com/dinakars777).
  * Gateway/session discovery: discover disk-only and retired ACP session stores under custom templated `session.store` roots so ACP reconciliation, session-id/session-label targeting, and run-id fallback keep working after restart. ([#44176](https://github.com/openclaw/openclaw/pull/44176)) thanks [@gumadeiras](https://github.com/gumadeiras).
  * Plugins/env-scoped roots: fix plugin discovery/load caches and provenance tracking so same-process `HOME`/`OPENCLAW_HOME` changes no longer reuse stale plugin state or misreport `~/...` plugins as untracked. ([#44046](https://github.com/openclaw/openclaw/pull/44046)) thanks [@gumadeiras](https://github.com/gumadeiras).
  * Models/OpenRouter native ids: canonicalize native OpenRouter model keys across config writes, runtime lookups, fallback management, and `models list --plain`, and migrate legacy duplicated `openrouter/openrouter/...` config entries forward on write.
  * Windows/native update: make package installs use the npm update path instead of the git path, carry portable Git into native Windows updates, and mirror the installer's Windows npm env so `openclaw update` no longer dies early on missing `git` or `node-llama-cpp` download setup.
  * Sandbox/write: preserve pinned mutation-helper payload stdin so sandboxed `write` no longer reports success while creating empty files. ([#43876](https://github.com/openclaw/openclaw/pull/43876)) Thanks [@glitch418x](https://github.com/glitch418x).
  * Security/exec approvals: escape invisible Unicode format characters in approval prompts so zero-width command text renders as visible `\u{...}` escapes instead of spoofing the reviewed command. (`GHSA-pcqg-f7rg-xfvv`)([#43687](https://github.com/openclaw/openclaw/pull/43687)) Thanks [@EkiXu](https://github.com/EkiXu) and [@vincentkoc](https://github.com/vincentkoc).
  * Hooks/loader: fail closed when workspace hook paths cannot be resolved with `realpath`, so unreadable or broken internal hook paths are skipped instead of falling back to unresolved imports. ([#44437](https://github.com/openclaw/openclaw/pull/44437)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Hooks/agent deliveries: dedupe repeated hook requests by optional idempotency key so webhook retries can reuse the first run instead of launching duplicate agent executions. ([#44438](https://github.com/openclaw/openclaw/pull/44438)) Thanks [@vincentkoc](https://github.com/vincentkoc).
  * Security/exec detection: normalize compatibility Unicode and strip invisible formatting code points before obfuscation checks so zero-width and fullwidth command tricks no longer suppress heuristic detection. (`GHSA-9r3v-37xh-2cf6`)([#44091](https://github.com/openclaw/openclaw/pull/44091)) Thanks [@wooluo](https://github.com/wooluo) and [@vincentkoc](https://github.com/vincentkoc).
  * Security/exec allowlist: preserve POSIX case sensitivity and keep `?` within a single path segment so exact-looking allowlist patterns no longer overmatch executables across case or directory boundaries. (`GHSA-f8r2-vg7x-gh8m`)([#43798](https://github.com/openclaw/openclaw/pull/43798)) Thanks [@zpbrent](https://github.com/zpbrent) and [@vincentkoc](https://github.com/vincentkoc).
  * Security/commands: require sender ownership for `/config` and `/debug` so authorized non-owner senders can no longer reach owner-only config and runtime debug surfaces. (`GHSA-r7vr-gr74-94p8`)([#44305](https://github.com/openclaw/openclaw/pull/44305)) Thanks [@tdjackey](https://github.com/tdjackey) and [@vincentkoc](https://github.com/vincentkoc).
  * Security/gateway auth: clear unbound client-declared scopes on shared-token WebSocket connects so device-less shared-token operators cannot self-declare elevated scopes. (`GHSA-rqpp-rjj8-7wv8`)([#44306](https://github.com/openclaw/openclaw/pull/44306)) Thanks [@LUOYEcode](https://github.com/LUOYEcode) and [@vincentkoc](https://github.com/vincentkoc).
  * Security/browser.request: block persistent browser profile create/delete routes from write-scoped `browser.request` so callers can no longer persist admin-only browser profile changes through the browser control surface. (`GHSA-vmhq-cqm9-6p7q`)([#43800](https://github.com/openclaw/openclaw/pull/43800)) Thanks [@tdjackey](https://github.com/tdjackey) and [@vincentkoc](https://github.com/vincentkoc).
  * Security/agent: reject public spawned-run lineage fields and keep workspace inheritance on the internal spawned-session path so external `agent` callers can no longer override the gateway workspace boundary. (`GHSA-2rqg-gjgv-84jm`)([#43801](https://github.com/openclaw/openclaw/pull/43801)) Thanks [@tdjackey](https://github.com/tdjackey) and [@vincentkoc](https://github.com/vincentkoc).
  * Security/session_status: enforce sandbox session-tree visibility and shared agent-to-agent access guards before reading or mutating target session state, so sandboxed subagents can no longer inspect parent session metadata or write parent model overrides via `session_status`. (`GHSA-wcxr-59v9-rxr8`)([#43754](https://github.com/openclaw/openclaw/pull/43754)) Thanks [@tdjackey](https://github.com/tdjackey) and [@vincentkoc](https://github.com/vincentkoc).
  * Security/agent tools: mark `nodes` as explicitly owner-only and document/test that `canvas` remains a shared trusted-operator surface unless a real boundary bypass exists.
  * Security/exec approvals: fail closed for Ruby approval flows that use `-r`, `--require`, or `-I` so approval-backed commands no longer bind only the main script while extra local code-...

[Read more](https://github.com/openclaw/openclaw/releases/tag/v2026.3.12)
### Contributors
  * [ ![@vincentkoc](https://avatars.githubusercontent.com/u/25068?s=64&v=4) ](https://github.com/vincentkoc)
  * [ ![@jriff](https://avatars.githubusercontent.com/u/50276?s=64&v=4) ](https://github.com/jriff)
  * [ ![@rodrigouroz](https://avatars.githubusercontent.com/u/384037?s=64&v=4) ](https://github.com/rodrigouroz)
  * [ ![@jalehman](https://avatars.githubusercontent.com/u/550978?s=64&v=4) ](https://github.com/jalehman)
  * [ ![@joshavant](https://avatars.githubusercontent.com/u/830519?s=64&v=4) ](https://github.com/joshavant)
  * [ ![@zpbrent](https://avatars.githubusercontent.com/u/834641?s=64&v=4) ](https://github.com/zpbrent)
  * [ ![@egkristi](https://avatars.githubusercontent.com/u/1047275?s=64&v=4) ](https://github.com/egkristi)
  * [ ![@ngutman](https://avatars.githubusercontent.com/u/1540134?s=64&v=4) ](https://github.com/ngutman)
  * [ ![@dzianisv](https://avatars.githubusercontent.com/u/2119348?s=64&v=4) ](https://github.com/dzianisv)
  * [ ![@pjeby](https://avatars.githubusercontent.com/u/3527052?s=64&v=4) ](https://github.com/pjeby)
  * [ ![@gumadeiras](https://avatars.githubusercontent.com/u/5599352?s=64&v=4) ](https://github.com/gumadeiras)
  * [ ![@BruceMacD](https://avatars.githubusercontent.com/u/5853428?s=64&v=4) ](https://github.com/BruceMacD)
  * [ ![@tdjackey](https://avatars.githubusercontent.com/u/6791132?s=64&v=4) ](https://github.com/tdjackey)
  * [ ![@wooluo](https://avatars.githubusercontent.com/u/8815032?s=64&v=4) ](https://github.com/wooluo)
  * [ ![@mathiasnagler](https://avatars.githubusercontent.com/u/9951231?s=64&v=4) ](https://github.com/mathiasnagler)
  * [ ![@vasujain00](https://avatars.githubusercontent.com/u/10598041?s=64&v=4) ](https://github.com/vasujain00)
  * [ ![@sallyom](https://avatars.githubusercontent.com/u/11166065?s=64&v=4) ](https://github.com/sallyom)
  * [ ![@obviyus](https://avatars.githubusercontent.com/u/22031114?s=64&v=4) ](https://github.com/obviyus)
  * [ ![@MoerAI](https://avatars.githubusercontent.com/u/26067127?s=64&v=4) ](https://github.com/MoerAI)
  * [ ![@TerminalsandCoffee](https://avatars.githubusercontent.com/u/26743149?s=64&v=4) ](https://github.com/TerminalsandCoffee)
  * [ ![@Cypherm](https://avatars.githubusercontent.com/u/28184436?s=64&v=4) ](https://github.com/Cypherm)
  * [ ![@EkiXu](https://avatars.githubusercontent.com/u/28667324?s=64&v=4) ](https://github.com/EkiXu)
  * [ ![@LyleLiu666](https://avatars.githubusercontent.com/u/31182860?s=64&v=4) ](https://github.com/LyleLiu666)
  * [ ![@Amineelfarssi](https://avatars.githubusercontent.com/u/49254916?s=64&v=4) ](https://github.com/Amineelfarssi)
  * [ ![@lisitan](https://avatars.githubusercontent.com/u/50470712?s=64&v=4) ](https://github.com/lisitan)
  * [ ![@opriz](https://avatars.githubusercontent.com/u/51957849?s=64&v=4) ](https://github.com/opriz)
  * [ ![@2233admin](https://avatars.githubusercontent.com/u/57929895?s=64&v=4) ](https://github.com/2233admin)
  * [ ![@BunsDev](https://avatars.githubusercontent.com/u/68980965?s=64&v=4) ](https://github.com/BunsDev)
  * [ ![@Nachx639](https://avatars.githubusercontent.com/u/71144023?s=64&v=4) ](https://github.com/Nachx639)
  * [ ![@openperf](https://avatars.githubusercontent.com/u/80630709?s=64&v=4) ](https://github.com/openperf)
  * [ ![@LUOYEcode](https://avatars.githubusercontent.com/u/93875149?s=64&v=4) ](https://github.com/LUOYEcode)
  * [ ![@hougangdev](https://avatars.githubusercontent.com/u/105773686?s=64&v=4) ](https://github.com/hougangdev)
  * [ ![@lintsinghua](https://avatars.githubusercontent.com/u/129816813?s=64&v=4) ](https://github.com/lintsinghua)
  * [ ![@shuicici](https://avatars.githubusercontent.com/u/157349610?s=64&v=4) ](https://github.com/shuicici)
  * [ ![@ez-lbz](https://avatars.githubusercontent.com/u/161842993?s=64&v=4) ](https://github.com/ez-lbz)
  * [ ![@glitch418x](https://avatars.githubusercontent.com/u/189487110?s=64&v=4) ](https://github.com/glitch418x)
  * [ ![@idimilabs](https://avatars.githubusercontent.com/u/229611532?s=64&v=4) ](https://github.com/idimilabs)
  * [ ![@dinakars777](https://avatars.githubusercontent.com/u/250428393?s=64&v=4) ](https://github.com/dinakars777)
  * [ ![@avirweb](https://avatars.githubusercontent.com/u/257412074?s=64&v=4) ](https://github.com/avirweb)
  * [ ![@chengzhichao-xydt](https://avatars.githubusercontent.com/u/264300353?s=64&v=4) ](https://github.com/chengzhichao-xydt)

vincentkoc, jriff, and 38 other contributors
Assets 6
Loading
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
👍 148 coygeek, Leon19960120, nalinduash, turtleqiu, coolwolfqs, Cheerwhy, hougangdev, Ghostwritten, LIHUA919, pigidser, and 138 more reacted with thumbs up emoji 😄 19 coygeek, coolwolfqs, lin72h, mdddj, shmilygkd, micah-sy, Endogen, lukas-h, NaveenPNair, usertlm, and 9 more reacted with laugh emoji 🎉 26 coygeek, gimlichael, nomowworriesco-stack, Lapot300, coolwolfqs, sahilsatralkar, shmilygkd, Endogen, lukas-h, NaveenPNair, and 16 more reacted with hooray emoji ❤️ 31 coygeek, JiaoCong9, apurvaumredkar, coolwolfqs, Vannakem2021, lin72h, shmilygkd, lukas-h, VanMinh-HNIMNAVGNAD, NaveenPNair, and 21 more reacted with heart emoji 🚀 24 coygeek, coolwolfqs, lin72h, shmilygkd, qcind, NaveenPNair, simonmiller6430-sys, Ness-Dawnastist, i-iooi-i, LloydNicholson, and 14 more reacted with rocket emoji 👀 16 coygeek, coolwolfqs, shmilygkd, rahmaneffendi446-arch, Puiching-Memory, banalord, NaveenPNair, Ness-Dawnastist, 1314mjf521, RamessesN, and 6 more reacted with eyes emoji
All reactions
  * 👍 148 reactions
  * 😄 19 reactions
  * 🎉 26 reactions
  * ❤️ 31 reactions
  * 🚀 24 reactions
  * 👀 16 reactions

192 people reacted
## openclaw 2026.3.11
12 Mar 05:07
![@steipete](https://avatars.githubusercontent.com/u/58493?s=40&v=4) [steipete](https://github.com/steipete)
Immutable release. Only release title and notes can be modified.
[ v2026.3.11  ](https://github.com/openclaw/openclaw/tree/v2026.3.11)
This tag was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
[ `29dc654`](https://github.com/openclaw/openclaw/commit/29dc65403faf41dc52944c02a0db9fa4b8457395)
This commit was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
Compare
#  Choose a tag to compare
## Sorry, something went wrong.
Filter
Loading
## Sorry, something went wrong.
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
## No results found
[View all tags](https://github.com/openclaw/openclaw/tags)
[openclaw 2026.3.11](https://github.com/openclaw/openclaw/releases/tag/v2026.3.11)
### Security
  * Gateway/WebSocket: enforce browser origin validation for all browser-originated connections regardless of whether proxy headers are present, closing a cross-site WebSocket hijacking path in `trusted-proxy` mode that could grant untrusted origins `operator.admin` access. ([GHSA-5wcw-8jjv-m286](https://github.com/advisories/GHSA-5wcw-8jjv-m286 "GHSA-5wcw-8jjv-m286"))

### Changes
  * OpenRouter/models: add temporary Hunter Alpha and Healer Alpha entries to the built-in catalog so OpenRouter users can try the new free stealth models during their roughly one-week availability window. ([#43642](https://github.com/openclaw/openclaw/pull/43642)) Thanks [@ping-Toven](https://github.com/ping-Toven).
  * iOS/Home canvas: add a bundled welcome screen with a live agent overview that refreshes on connect, reconnect, and foreground return, and move the compact connection pill off the top-left canvas overlay. ([#42456](https://github.com/openclaw/openclaw/pull/42456)) Thanks [@ngutman](https://github.com/ngutman).
  * iOS/Home canvas: replace floating controls with a docked toolbar, make the bundled home scaffold adapt to smaller phones, and open chat in the resolved main session instead of a synthetic `ios` session. ([#42456](https://github.com/openclaw/openclaw/pull/42456)) Thanks [@ngutman](https://github.com/ngutman).
  * macOS/chat UI: add a chat model picker, persist explicit thinking-level selections across relaunch, and harden provider-aware session model sync for the shared chat composer. ([#42314](https://github.com/openclaw/openclaw/pull/42314)) Thanks [@ImLukeF](https://github.com/ImLukeF).
  * Onboarding/Ollama: add first-class Ollama setup with Local or Cloud + Local modes, browser-based cloud sign-in, curated model suggestions, and cloud-model handling that skips unnecessary local pulls. ([#41529](https://github.com/openclaw/openclaw/pull/41529)) Thanks [@BruceMacD](https://github.com/BruceMacD).
  * OpenCode/onboarding: add new OpenCode Go provider, treat Zen and Go as one OpenCode setup in the wizard/docs while keeping the runtime providers split, store one shared OpenCode key for both profiles, and stop overriding the built-in `opencode-go` catalog routing. ([#42313](https://github.com/openclaw/openclaw/pull/42313)) Thanks [@ImLukeF](https://github.com/ImLukeF) and [@vincentkoc](https://github.com/vincentkoc).
  * Memory: add opt-in multimodal image and audio indexing for `memorySearch.extraPaths` with Gemini `gemini-embedding-2-preview`, strict fallback gating, and scope-based reindexing. ([#43460](https://github.com/openclaw/openclaw/pull/43460)) Thanks [@gumadeiras](https://github.com/gumadeiras).
  * Memory/Gemini: add `gemini-embedding-2-preview` memory-search support with configurable output dimensions and automatic reindexing when the configured dimensions change. ([#42501](https://github.com/openclaw/openclaw/pull/42501)) Thanks [@BillChirico](https://github.com/BillChirico) and [@gumadeiras](https://github.com/gumadeiras).
  * macOS/onboarding: detect when remote gateways need a shared auth token, explain where to find it on the gateway host, and clarify when a successful check used paired-device auth instead. ([#43100](https://github.com/openclaw/openclaw/pull/43100)) Thanks [@ngutman](https://github.com/ngutman).
  * Discord/auto threads: add `autoArchiveDuration` channel config for auto-created threads so Discord thread archiving can stay at 1 hour, 1 day, 3 days, or 1 week instead of always using the 1-hour default. ([#35065](https://github.com/openclaw/openclaw/pull/35065)) Thanks [@davidguttman](https://github.com/davidguttman).
  * iOS/TestFlight: add a local beta release flow with Fastlane prepare/archive/upload support, canonical beta bundle IDs, and watch-app archive fixes. ([#42991](https://github.com/openclaw/openclaw/pull/42991)) Thanks [@ngutman](https://github.com/ngutman).
  * ACP/sessions_spawn: add optional `resumeSessionId` for `runtime: "acp"` so spawned ACP sessions can resume an existing ACPX/Codex conversation instead of always starting fresh. ([#41847](https://github.com/openclaw/openclaw/pull/41847)) Thanks [@pejmanjohn](https://github.com/pejmanjohn).
  * Gateway/node pending work: add narrow in-memory pending-work queue primitives (`node.pending.enqueue` / `node.pending.drain`) and wake-helper reuse as a foundation for dormant-node work delivery. ([#41409](https://github.com/openclaw/openclaw/pull/41409)) Thanks [@mbelinky](https://github.com/mbelinky).
  * Git/runtime state: ignore the gateway-generated `.dev-state` file so local runtime state does not show up as untracked repo noise. ([#41848](https://github.com/openclaw/openclaw/pull/41848)) Thanks [@smysle](https://github.com/smysle).
  * Exec/child commands: mark child command environments with `OPENCLAW_CLI` so subprocesses can detect when they were launched from the OpenClaw CLI. ([#41411](https://github.com/openclaw/openclaw/pull/41411)) Thanks [@vincentkoc](https://github.com/vincentkoc).

### Breaking
  * Cron/doctor: tighten isolated cron delivery so cron jobs can no longer notify through ad hoc agent sends or fallback main-session summaries, and add `openclaw doctor --fix` migration for legacy cron storage and legacy notify/webhook delivery metadata. ([#40998](https://github.com/openclaw/openclaw/pull/40998)) Thanks [@mbelinky](https://github.com/mbelinky).

### Fixes
  * Agents/text sanitization: strip leaked model control tokens (`<|...|>` and full-width `<｜...｜>` variants) from user-facing assistant text, preventing GLM-5 and DeepSeek internal delimiters from reaching end users. ([#42173](https://github.com/openclaw/openclaw/pull/42173)) Thanks [@imwyvern](https://github.com/imwyvern).
  * iOS/gateway foreground recovery: reconnect immediately on foreground return after stale background sockets are torn down, so the app no longer stays disconnected until a later wake path happens. ([#41384](https://github.com/openclaw/openclaw/pull/41384)) Thanks [@mbelinky](https://github.com/mbelinky).
  * Gateway/Control UI: keep dashboard auth tokens in session-scoped browser storage so same-tab refreshes preserve remote token auth without restoring long-lived localStorage token persistence, while scoping tokens to the selected gateway URL and fragment-only bootstrap flow. ([#40892](https://github.com/openclaw/openclaw/pull/40892)) thanks [@velvet-shark](https://github.com/velvet-shark).
  * Gateway/macOS launchd restarts: keep the LaunchAgent registered during explicit restarts, hand off self-restarts through a detached launchd helper, and recover config/hot reload restart paths without unloading the service. Fixes [#43311](https://github.com/openclaw/openclaw/issues/43311), [#43406](https://github.com/openclaw/openclaw/issues/43406), [#43035](https://github.com/openclaw/openclaw/issues/43035), and [#43049](https://github.com/openclaw/openclaw/issues/43049).
  * macOS/LaunchAgent install: tighten LaunchAgent directory and plist permissions during install so launchd bootstrap does not fail when the target home path or generated plist inherited group/world-writable modes.
  * Discord/reply chunking: resolve the effective `maxLinesPerMessage` config across live reply paths and preserve `chunkMode` in the fast send path so long Discord replies no longer split unexpectedly at the default 17-line limit. ([#40133](https://github.com/openclaw/openclaw/pull/40133)) thanks [@rbutera](https://github.com/rbutera).
  * Feishu/local image auto-convert: pass `mediaLocalRoots` through the `sendText` local-image shim so allowed local image paths upload as Feishu images again instead of falling back to raw path text. ([#40623](https://github.com/openclaw/openclaw/pull/40623)) Thanks [@ayanesakura](https://github.com/ayanesakura).
  * Models/Kimi Coding: send `anthropic-messages` tools in native Anthropic format again so `kimi-coding` stops degrading tool calls into XML/plain-text pseudo invocations instead of real `tool_use` blocks. ([#38669](https://github.com/openclaw/openclaw/issues/38669), [#39907](https://github.com/openclaw/openclaw/issues/39907), [#40552](https://github.com/openclaw/openclaw/issues/40552)) Thanks [@opriz](https://github.com/opriz).
  * Telegram/outbound HTML sends: chunk long HTML-mode messages, preserve plain-text fallback and silent-delivery params across retries, and cut over to plain text when HTML chunk planning cannot safely preserve the full message. ([#42240](https://github.com/openclaw/openclaw/pull/42240)) thanks [@obviyus](https://github.com/obviyus).
  * Telegram/final preview delivery: split active preview lifecycle from cleanup retention so missing archived preview edits avoid duplicate fallback sends without clearing the live preview or blocking later in-place finalization. ([#41662](https://github.com/openclaw/openclaw/pull/41662)) thanks [@hougangdev](https://github.com/hougangdev).
  * Telegram/final preview delivery followup: keep ambiguous missing-`message_id` finals only when a preview was already visible, while first-preview/no-id cases still fall back so Telegram users do not lose the final reply. ([#41932](https://github.com/openclaw/openclaw/pull/41932)) thanks [@hougangdev](https://github.com/hougangdev).
  * Telegram/final preview cleanup follow-up: clear stale cleanup-retain state only for transient preview finals so archived-preview retains no longer leave a stale partial bubble beside a later fallback-sent final. ([#41763](https://github.com/openclaw/openclaw/pull/41763)) Thanks [@obviyus](https://github.com/obviyus).
  * Gateway/auth: allow one trusted device-token retry on shared-token mismatch with recovery hints to prevent reconnect churn during token drift. ([#42507](https://github.com/openclaw/openclaw/pull/42507)) Thanks [@joshavant](https://github.com/joshavant).
  * Gateway/config errors: surface up to three validation issues in top-level `config.set`, `config.patch`, and `config.apply` error messages while preserving structured issue details. ([#42664](https://github.com/openclaw/openclaw/pull/42664)) Thanks [@huntharo](https://github.com/huntharo).
  * Agents/Azure OpenAI Responses: include the `azure-openai` provider in the Responses API store override so Azure OpenAI multi-turn cron jobs and embedded agent runs no longer fail with HTTP 400 "store is set to false". ([#42934](https://github.com/openclaw/openclaw/pull/42934), fixes [#42800](https://github.com/openclaw/openclaw/issues/42800)) Thanks [@ademczuk](https://github.com/ademczuk).
  * Agents/error rendering: ignore stale assistant `errorMessage` fields on successful turns so background/tool-side failures no longer prepend synthetic billing errors over valid replies. ([#40616](https://github.com/openclaw/openclaw/pull/40616)) Thanks [@ingyukoh](https://github.com/ingyukoh).
  * Agents/billing recovery: probe single-provider billing cooldowns on the existing throttle so topping up credits can recover without a manual gateway restart. ([#41422](https://github.com/openclaw/openclaw/pull/41422)) thanks [@altaywtf](https://github.com/altaywtf).
  * Agents/fallback: treat HTTP 499 responses as transient in both raw-text and structured failover paths so Anthropic-style client-closed overload responses trigger model fallback reliably. ([#41468](https://github.com/openclaw/openclaw/pull/41468)) thanks [@zeroasterisk](https://github.com/zeroasterisk).
  * Agents/fallback: recognize Venice `402 Insufficient USD or Diem balance` billing errors so configured model fallbacks trigger instead of surfacing the raw provider error. ([#43205](https://github.com/openclaw/openclaw/pull/43205)) Thanks [@Squabble9](https://github.com/Squabble9).
  * Agents/fallback: recognize Poe `402 You've used up your points!` billing errors so configured model fallbacks trigger instead of surfacing the raw provider error. ([#42278](https://github.com/openclaw/openclaw/pull/42278)) Thanks [@CryUshio](https://github.com/CryUshio).
  * Agents/failover: treat Gemini `MALFORMED_RESPONSE` stop reasons as retryable timeouts so preview-model enum drift falls back cleanly instead of crashing the run, without also reclassifying malformed function-call errors. ([#42292](https://github.com/openclaw/openclaw/pull/42292)) Thanks [@jnMetaCode](https://github.com/jnMetaCode).
  * Agents/cooldowns: default cooldown windows with no recorded failure history to `unknown` instead of `rate_limit`, avoiding false API rate-limit warnings while preserving cooldown recovery probes. ([#42911](https://github.com/openclaw/openclaw/pull/42911)) Thanks [@VibhorGautam](https://github.com/VibhorGautam).
  * Auth/cooldowns: reset expired auth-profile cooldown error counters before computing the next backoff so stale on-disk counters do not re-escalate into long cooldown loops after expiry. ([#41028](https://github.com/openclaw/openclaw/pull/41028)) thanks [@zerone0x](https://github.com/zerone0x).
  * Agents/memory flush: forward `memoryFlushWritePath` through `runEmbeddedPiAgent` so memory-triggered flush turns keep the append-only write guard without aborting before tool setup. Follows up on [#38574](https://github.com/openclaw/openclaw/pull/38574). ([#41761](https://github.com/openclaw/openclaw/pull/41761)) Thanks [@frankekn](https://github.com/frankekn).
  * Agents/context pruning: prune image-only tool results during soft-trim, align context-pruning coverage with the new tool-result contract, and extend historical image cleanup to the same screenshot-heavy session path. ([#43045](https://github.com/openclaw/openclaw/pull/43045)) Thanks [@MoerAI](https://github.com/MoerAI).
  * Sessions/reset model recompute: clear stale runtime model, context-token, and system-prompt metadata before session resets recompute the replacement session, so resets pick up current defaults and explicit overrides instead of reusing old runtime model state. ([#41173](https://github.com/openclaw/openclaw/pull/41173)) thanks [@pon](https://github.com/pon)...

[Read more](https://github.com/openclaw/openclaw/releases/tag/v2026.3.11)
### Contributors
  * [ ![@zeroasterisk](https://avatars.githubusercontent.com/u/23422?s=64&v=4) ](https://github.com/zeroasterisk)
  * [ ![@vincentkoc](https://avatars.githubusercontent.com/u/25068?s=64&v=4) ](https://github.com/vincentkoc)
  * [ ![@velvet-shark](https://avatars.githubusercontent.com/u/126378?s=64&v=4) ](https://github.com/velvet-shark)
  * [ ![@davidguttman](https://avatars.githubusercontent.com/u/431696?s=64&v=4) ](https://github.com/davidguttman)
  * [ ![@mvanhorn](https://avatars.githubusercontent.com/u/455140?s=64&v=4) ](https://github.com/mvanhorn)
  * [ ![@pejmanjohn](https://avatars.githubusercontent.com/u/481729?s=64&v=4) ](https://github.com/pejmanjohn)
  * [ ![@xinhuagu](https://avatars.githubusercontent.com/u/562450?s=64&v=4) ](https://github.com/xinhuagu)
  * [ ![@joshavant](https://avatars.githubusercontent.com/u/830519?s=64&v=4) ](https://github.com/joshavant)
  * [ ![@kyohwang](https://avatars.githubusercontent.com/u/1436387?s=64&v=4) ](https://github.com/kyohwang)
  * [ ![@ngutman](https://avatars.githubusercontent.com/u/1540134?s=64&v=4) ](https://github.com/ngutman)
  * [ ![@imwyvern](https://avatars.githubusercontent.com/u/1765672?s=64&v=4) ](https://github.com/imwyvern)
  * [ ![@andyliu](https://avatars.githubusercontent.com/u/2377291?s=64&v=4) ](https://github.com/andyliu)
  * [ ![@hnykda](https://avatars.githubusercontent.com/u/2741256?s=64&v=4) ](https://github.com/hnykda)
  * [ ![@BradGroux](https://avatars.githubusercontent.com/u/3053586?s=64&v=4) ](https://github.com/BradGroux)
  * [ ![@jackal092927](https://avatars.githubusercontent.com/u/3854860?s=64&v=4) ](https://github.com/jackal092927)
  * [ ![@sircrumpet](https://avatars.githubusercontent.com/u/4436535?s=64&v=4) ](https://github.com/sircrumpet)
  * [ ![@frankekn](https://avatars.githubusercontent.com/u/4488090?s=64&v=4) ](https://github.com/frankekn)
  * [ ![@ademczuk](https://avatars.githubusercontent.com/u/5212682?s=64&v=4) ](https://github.com/ademczuk)
  * [ ![@gumadeiras](https://avatars.githubusercontent.com/u/5599352?s=64&v=4) ](https://github.com/gumadeiras)
  * [ ![@huntharo](https://avatars.githubusercontent.com/u/5617868?s=64&v=4) ](https://github.com/huntharo)
  * [ ![@BruceMacD](https://avatars.githubusercontent.com/u/5853428?s=64&v=4) ](https://github.com/BruceMacD)
  * [ ![@ingyukoh](https://avatars.githubusercontent.com/u/6015960?s=64&v=4) ](https://github.com/ingyukoh)
  * [ ![@rbutera](https://avatars.githubusercontent.com/u/6047293?s=64&v=4) ](https://github.com/rbutera)
  * [ ![@tdjackey](https://avatars.githubusercontent.com/u/6791132?s=64&v=4) ](https://github.com/tdjackey)
  * [ ![@altaywtf](https://avatars.githubusercontent.com/u/9790196?s=64&v=4) ](https://github.com/altaywtf)
  * [ ![@pomelo-nwu](https://avatars.githubusercontent.com/u/10703060?s=64&v=4) ](https://github.com/pomelo-nwu)
  * [ ![@benjipeng](https://avatars.githubusercontent.com/u/11394934?s=64&v=4) ](https://github.com/benjipeng)
  * [ ![@jnMetaCode](https://avatars.githubusercontent.com/u/12096460?s=64&v=4) ](https://github.com/jnMetaCode)
  * [ ![@BillChirico](https://avatars.githubusercontent.com/u/13951316?s=64&v=4) ](https://github.com/BillChirico)
  * [ ![@zheliu2](https://avatars.githubusercontent.com/u/15888718?s=64&v=4) ](https://github.com/zheliu2)
  * [ ![@jiarung](https://avatars.githubusercontent.com/u/16461359?s=64&v=4) ](https://github.com/jiarung)
  * [ ![@obviyus](https://avatars.githubusercontent.com/u/22031114?s=64&v=4) ](https://github.com/obviyus)
  * [ ![@MoerAI](https://avatars.githubusercontent.com/u/26067127?s=64&v=4) ](https://github.com/MoerAI)
  * [ ![@CryUshio](https://avatars.githubusercontent.com/u/30655354?s=64&v=4) ](https://github.com/CryUshio)
  * [ ![@urianpaul94](https://avatars.githubusercontent.com/u/33277984?s=64&v=4) ](https://github.com/urianpaul94)
  * [ ![@zhoulf1006](https://avatars.githubusercontent.com/u/35586967?s=64&v=4) ](https://github.com/zhoulf1006)
  * [ ![@cgdusek](https://avatars.githubusercontent.com/u/38732970?s=64&v=4) ](https://github.com/cgdusek)
  * [ ![@zerone0x](https://avatars.githubusercontent.com/u/39543393?s=64&v=4) ](https://github.com/zerone0x)
  * [ ![@ayanesakura](https://avatars.githubusercontent.com/u/40628300?s=64&v=4) ](https://github.com/ayanesakura)
  * [ ![@ApacheBin](https://avatars.githubusercontent.com/u/43498191?s=64&v=4) ](https://github.com/ApacheBin)
  * [ ![@davidrudduck](https://avatars.githubusercontent.com/u/47308254?s=64&v=4) ](https://github.com/davidrudduck)
  * [ ![@opriz](https://avatars.githubusercontent.com/u/51957849?s=64&v=4) ](https://github.com/opriz)
  * [ ![@VibhorGautam](https://avatars.githubusercontent.com/u/55019395?s=64&v=4) ](https://github.com/VibhorGautam)
  * [ ![@BunsDev](https://avatars.githubusercontent.com/u/68980965?s=64&v=4) ](https://github.com/BunsDev)
  * [ ![@ping-Toven](https://avatars.githubusercontent.com/u/69218856?s=64&v=4) ](https://github.com/ping-Toven)
  * [ ![@Julbarth](https://avatars.githubusercontent.com/u/72460857?s=64&v=4) ](https://github.com/Julbarth)
  * [ ![@laurieluo](https://avatars.githubusercontent.com/u/89195476?s=64&v=4) ](https://github.com/laurieluo)
  * [ ![@ImLukeF](https://avatars.githubusercontent.com/u/92253590?s=64&v=4) ](https://github.com/ImLukeF)
  * [ ![@hougangdev](https://avatars.githubusercontent.com/u/105773686?s=64&v=4) ](https://github.com/hougangdev)
  * [ ![@Jimmy-xuzimo](https://avatars.githubusercontent.com/u/111618279?s=64&v=4) ](https://github.com/Jimmy-xuzimo)
  * [ ![@mbelinky](https://avatars.githubusercontent.com/u/132747814?s=64&v=4) ](https://github.com/mbelinky)
  * [ ![@Squabble9](https://avatars.githubusercontent.com/u/194720422?s=64&v=4) ](https://github.com/Squabble9)
  * [ ![@smysle](https://avatars.githubusercontent.com/u/207193754?s=64&v=4) ](https://github.com/smysle)
  * [ ![@dsantoreis](https://avatars.githubusercontent.com/u/220753637?s=64&v=4) ](https://github.com/dsantoreis)
  * [ ![@futuremind2026](https://avatars.githubusercontent.com/u/258860756?s=64&v=4) ](https://github.com/futuremind2026)
  * [ ![@echo931](https://avatars.githubusercontent.com/u/259437483?s=64&v=4) ](https://github.com/echo931)
  * [ ![@dutifulbob](https://avatars.githubusercontent.com/u/261991368?s=64&v=4) ](https://github.com/dutifulbob)
  * [ ![@xaeon2026](https://avatars.githubusercontent.com/u/264572156?s=64&v=4) ](https://github.com/xaeon2026)
  * [ ![@PonyX-lab](https://avatars.githubusercontent.com/u/266766228?s=64&v=4) ](https://github.com/PonyX-lab)

zeroasterisk, vincentkoc, and 57 other contributors
Assets 3
Loading
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
👍 189 coygeek, soumikbhatta, nhmpk824-gif, dxsup, W1595159, frannnnk, songtao98, leeduyoung, darek8686, editbyjunior, and 179 more reacted with thumbs up emoji 😄 18 coygeek, W1595159, eason-lee, orwiso, xwz07022, mdddj, lin72h, qcind, hussamgalal999, birdofprey, and 8 more reacted with laugh emoji 🎉 25 coygeek, soumikbhatta, thanhle98, Kaven9, aipwp-claw, W1595159, EscalioDev, zyk1172, alexivanov-ai, tonisole, and 15 more reacted with hooray emoji ❤️ 23 Vannakem2021, coygeek, robleo50, W1595159, TianQingX, zyk1172, alexivanov-ai, Laminua, mdddj, lin72h, and 13 more reacted with heart emoji 🚀 21 coygeek, W1595159, lexafaxine, mdddj, Stanley-blik, lin72h, i-iooi-i, kidroca, LloydNicholson, birdofprey, and 11 more reacted with rocket emoji 👀 14 coygeek, jimweaver, vucat12, Zmin2003, W1595159, beforeugone520, Puiching-Memory, lib3yu, yigerende, mdddj, and 4 more reacted with eyes emoji
All reactions
  * 👍 189 reactions
  * 😄 18 reactions
  * 🎉 25 reactions
  * ❤️ 23 reactions
  * 🚀 21 reactions
  * 👀 14 reactions

236 people reacted
## openclaw 2026.3.11-beta.1
12 Mar 04:23
![@steipete](https://avatars.githubusercontent.com/u/58493?s=40&v=4) [steipete](https://github.com/steipete)
Immutable release. Only release title and notes can be modified.
[ v2026.3.11-beta.1  ](https://github.com/openclaw/openclaw/tree/v2026.3.11-beta.1)
This tag was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
[ `b125c3b`](https://github.com/openclaw/openclaw/commit/b125c3ba065752c493bb763ac2f0a5e82ed3d0ae)
This commit was signed with the committer’s **verified signature**.
[ ![](https://avatars.githubusercontent.com/u/58493?s=64&v=4) ](https://github.com/steipete) [steipete](https://github.com/steipete) Peter Steinberger
SSH Key Fingerprint: WmI9lVtd7F2c5XyRHbZVO3yYYJzwsSNzcZQMPT147HI
Verified
[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).
Compare
#  Choose a tag to compare
## Sorry, something went wrong.
Filter
Loading
## Sorry, something went wrong.
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
## No results found
[View all tags](https://github.com/openclaw/openclaw/tags)
[openclaw 2026.3.11-beta.1](https://github.com/openclaw/openclaw/releases/tag/v2026.3.11-beta.1) Pre-release
Pre-release
### Security
  * Gateway/WebSocket: enforce browser origin validation for all browser-originated connections regardless of whether proxy headers are present, closing a cross-site WebSocket hijacking path in `trusted-proxy` mode that could grant untrusted origins `operator.admin` access. ([GHSA-5wcw-8jjv-m286](https://github.com/advisories/GHSA-5wcw-8jjv-m286 "GHSA-5wcw-8jjv-m286"))

### Changes
  * OpenRouter/models: add temporary Hunter Alpha and Healer Alpha entries to the built-in catalog so OpenRouter users can try the new free stealth models during their roughly one-week availability window. ([#43642](https://github.com/openclaw/openclaw/pull/43642)) Thanks [@ping-Toven](https://github.com/ping-Toven).
  * iOS/Home canvas: add a bundled welcome screen with a live agent overview that refreshes on connect, reconnect, and foreground return, and move the compact connection pill off the top-left canvas overlay. ([#42456](https://github.com/openclaw/openclaw/pull/42456)) Thanks [@ngutman](https://github.com/ngutman).
  * iOS/Home canvas: replace floating controls with a docked toolbar, make the bundled home scaffold adapt to smaller phones, and open chat in the resolved main session instead of a synthetic `ios` session. ([#42456](https://github.com/openclaw/openclaw/pull/42456)) Thanks [@ngutman](https://github.com/ngutman).
  * macOS/chat UI: add a chat model picker, persist explicit thinking-level selections across relaunch, and harden provider-aware session model sync for the shared chat composer. ([#42314](https://github.com/openclaw/openclaw/pull/42314)) Thanks [@ImLukeF](https://github.com/ImLukeF).
  * Onboarding/Ollama: add first-class Ollama setup with Local or Cloud + Local modes, browser-based cloud sign-in, curated model suggestions, and cloud-model handling that skips unnecessary local pulls. ([#41529](https://github.com/openclaw/openclaw/pull/41529)) Thanks [@BruceMacD](https://github.com/BruceMacD).
  * OpenCode/onboarding: add new OpenCode Go provider, treat Zen and Go as one OpenCode setup in the wizard/docs while keeping the runtime providers split, store one shared OpenCode key for both profiles, and stop overriding the built-in `opencode-go` catalog routing. ([#42313](https://github.com/openclaw/openclaw/pull/42313)) Thanks [@ImLukeF](https://github.com/ImLukeF) and [@vincentkoc](https://github.com/vincentkoc).
  * Memory: add opt-in multimodal image and audio indexing for `memorySearch.extraPaths` with Gemini `gemini-embedding-2-preview`, strict fallback gating, and scope-based reindexing. ([#43460](https://github.com/openclaw/openclaw/pull/43460)) Thanks [@gumadeiras](https://github.com/gumadeiras).
  * Memory/Gemini: add `gemini-embedding-2-preview` memory-search support with configurable output dimensions and automatic reindexing when the configured dimensions change. ([#42501](https://github.com/openclaw/openclaw/pull/42501)) Thanks [@BillChirico](https://github.com/BillChirico) and [@gumadeiras](https://github.com/gumadeiras).
  * macOS/onboarding: detect when remote gateways need a shared auth token, explain where to find it on the gateway host, and clarify when a successful check used paired-device auth instead. ([#43100](https://github.com/openclaw/openclaw/pull/43100)) Thanks [@ngutman](https://github.com/ngutman).
  * Discord/auto threads: add `autoArchiveDuration` channel config for auto-created threads so Discord thread archiving can stay at 1 hour, 1 day, 3 days, or 1 week instead of always using the 1-hour default. ([#35065](https://github.com/openclaw/openclaw/pull/35065)) Thanks [@davidguttman](https://github.com/davidguttman).
  * iOS/TestFlight: add a local beta release flow with Fastlane prepare/archive/upload support, canonical beta bundle IDs, and watch-app archive fixes. ([#42991](https://github.com/openclaw/openclaw/pull/42991)) Thanks [@ngutman](https://github.com/ngutman).
  * ACP/sessions_spawn: add optional `resumeSessionId` for `runtime: "acp"` so spawned ACP sessions can resume an existing ACPX/Codex conversation instead of always starting fresh. ([#41847](https://github.com/openclaw/openclaw/pull/41847)) Thanks [@pejmanjohn](https://github.com/pejmanjohn).
  * Gateway/node pending work: add narrow in-memory pending-work queue primitives (`node.pending.enqueue` / `node.pending.drain`) and wake-helper reuse as a foundation for dormant-node work delivery. ([#41409](https://github.com/openclaw/openclaw/pull/41409)) Thanks [@mbelinky](https://github.com/mbelinky).
  * Git/runtime state: ignore the gateway-generated `.dev-state` file so local runtime state does not show up as untracked repo noise. ([#41848](https://github.com/openclaw/openclaw/pull/41848)) Thanks [@smysle](https://github.com/smysle).
  * Exec/child commands: mark child command environments with `OPENCLAW_CLI` so subprocesses can detect when they were launched from the OpenClaw CLI. ([#41411](https://github.com/openclaw/openclaw/pull/41411)) Thanks [@vincentkoc](https://github.com/vincentkoc).

### Breaking
  * Cron/doctor: tighten isolated cron delivery so cron jobs can no longer notify through ad hoc agent sends or fallback main-session summaries, and add `openclaw doctor --fix` migration for legacy cron storage and legacy notify/webhook delivery metadata. ([#40998](https://github.com/openclaw/openclaw/pull/40998)) Thanks [@mbelinky](https://github.com/mbelinky).

### Fixes
  * Agents/text sanitization: strip leaked model control tokens (`<|...|>` and full-width `<｜...｜>` variants) from user-facing assistant text, preventing GLM-5 and DeepSeek internal delimiters from reaching end users. ([#42173](https://github.com/openclaw/openclaw/pull/42173)) Thanks [@imwyvern](https://github.com/imwyvern).
  * iOS/gateway foreground recovery: reconnect immediately on foreground return after stale background sockets are torn down, so the app no longer stays disconnected until a later wake path happens. ([#41384](https://github.com/openclaw/openclaw/pull/41384)) Thanks [@mbelinky](https://github.com/mbelinky).
  * Gateway/Control UI: keep dashboard auth tokens in session-scoped browser storage so same-tab refreshes preserve remote token auth without restoring long-lived localStorage token persistence, while scoping tokens to the selected gateway URL and fragment-only bootstrap flow. ([#40892](https://github.com/openclaw/openclaw/pull/40892)) thanks [@velvet-shark](https://github.com/velvet-shark).
  * Gateway/macOS launchd restarts: keep the LaunchAgent registered during explicit restarts, hand off self-restarts through a detached launchd helper, and recover config/hot reload restart paths without unloading the service. Fixes [#43311](https://github.com/openclaw/openclaw/issues/43311), [#43406](https://github.com/openclaw/openclaw/issues/43406), [#43035](https://github.com/openclaw/openclaw/issues/43035), and [#43049](https://github.com/openclaw/openclaw/issues/43049).
  * macOS/LaunchAgent install: tighten LaunchAgent directory and plist permissions during install so launchd bootstrap does not fail when the target home path or generated plist inherited group/world-writable modes.
  * Discord/reply chunking: resolve the effective `maxLinesPerMessage` config across live reply paths and preserve `chunkMode` in the fast send path so long Discord replies no longer split unexpectedly at the default 17-line limit. ([#40133](https://github.com/openclaw/openclaw/pull/40133)) thanks [@rbutera](https://github.com/rbutera).
  * Feishu/local image auto-convert: pass `mediaLocalRoots` through the `sendText` local-image shim so allowed local image paths upload as Feishu images again instead of falling back to raw path text. ([#40623](https://github.com/openclaw/openclaw/pull/40623)) Thanks [@ayanesakura](https://github.com/ayanesakura).
  * Models/Kimi Coding: send `anthropic-messages` tools in native Anthropic format again so `kimi-coding` stops degrading tool calls into XML/plain-text pseudo invocations instead of real `tool_use` blocks. ([#38669](https://github.com/openclaw/openclaw/issues/38669), [#39907](https://github.com/openclaw/openclaw/issues/39907), [#40552](https://github.com/openclaw/openclaw/issues/40552)) Thanks [@opriz](https://github.com/opriz).
  * Telegram/outbound HTML sends: chunk long HTML-mode messages, preserve plain-text fallback and silent-delivery params across retries, and cut over to plain text when HTML chunk planning cannot safely preserve the full message. ([#42240](https://github.com/openclaw/openclaw/pull/42240)) thanks [@obviyus](https://github.com/obviyus).
  * Telegram/final preview delivery: split active preview lifecycle from cleanup retention so missing archived preview edits avoid duplicate fallback sends without clearing the live preview or blocking later in-place finalization. ([#41662](https://github.com/openclaw/openclaw/pull/41662)) thanks [@hougangdev](https://github.com/hougangdev).
  * Telegram/final preview delivery followup: keep ambiguous missing-`message_id` finals only when a preview was already visible, while first-preview/no-id cases still fall back so Telegram users do not lose the final reply. ([#41932](https://github.com/openclaw/openclaw/pull/41932)) thanks [@hougangdev](https://github.com/hougangdev).
  * Telegram/final preview cleanup follow-up: clear stale cleanup-retain state only for transient preview finals so archived-preview retains no longer leave a stale partial bubble beside a later fallback-sent final. ([#41763](https://github.com/openclaw/openclaw/pull/41763)) Thanks [@obviyus](https://github.com/obviyus).
  * Gateway/auth: allow one trusted device-token retry on shared-token mismatch with recovery hints to prevent reconnect churn during token drift. ([#42507](https://github.com/openclaw/openclaw/pull/42507)) Thanks [@joshavant](https://github.com/joshavant).
  * Gateway/config errors: surface up to three validation issues in top-level `config.set`, `config.patch`, and `config.apply` error messages while preserving structured issue details. ([#42664](https://github.com/openclaw/openclaw/pull/42664)) Thanks [@huntharo](https://github.com/huntharo).
  * Agents/Azure OpenAI Responses: include the `azure-openai` provider in the Responses API store override so Azure OpenAI multi-turn cron jobs and embedded agent runs no longer fail with HTTP 400 "store is set to false". ([#42934](https://github.com/openclaw/openclaw/pull/42934), fixes [#42800](https://github.com/openclaw/openclaw/issues/42800)) Thanks [@ademczuk](https://github.com/ademczuk).
  * Agents/error rendering: ignore stale assistant `errorMessage` fields on successful turns so background/tool-side failures no longer prepend synthetic billing errors over valid replies. ([#40616](https://github.com/openclaw/openclaw/pull/40616)) Thanks [@ingyukoh](https://github.com/ingyukoh).
  * Agents/billing recovery: probe single-provider billing cooldowns on the existing throttle so topping up credits can recover without a manual gateway restart. ([#41422](https://github.com/openclaw/openclaw/pull/41422)) thanks [@altaywtf](https://github.com/altaywtf).
  * Agents/fallback: treat HTTP 499 responses as transient in both raw-text and structured failover paths so Anthropic-style client-closed overload responses trigger model fallback reliably. ([#41468](https://github.com/openclaw/openclaw/pull/41468)) thanks [@zeroasterisk](https://github.com/zeroasterisk).
  * Agents/fallback: recognize Venice `402 Insufficient USD or Diem balance` billing errors so configured model fallbacks trigger instead of surfacing the raw provider error. ([#43205](https://github.com/openclaw/openclaw/pull/43205)) Thanks [@Squabble9](https://github.com/Squabble9).
  * Agents/fallback: recognize Poe `402 You've used up your points!` billing errors so configured model fallbacks trigger instead of surfacing the raw provider error. ([#42278](https://github.com/openclaw/openclaw/pull/42278)) Thanks [@CryUshio](https://github.com/CryUshio).
  * Agents/failover: treat Gemini `MALFORMED_RESPONSE` stop reasons as retryable timeouts so preview-model enum drift falls back cleanly instead of crashing the run, without also reclassifying malformed function-call errors. ([#42292](https://github.com/openclaw/openclaw/pull/42292)) Thanks [@jnMetaCode](https://github.com/jnMetaCode).
  * Agents/cooldowns: default cooldown windows with no recorded failure history to `unknown` instead of `rate_limit`, avoiding false API rate-limit warnings while preserving cooldown recovery probes. ([#42911](https://github.com/openclaw/openclaw/pull/42911)) Thanks [@VibhorGautam](https://github.com/VibhorGautam).
  * Auth/cooldowns: reset expired auth-profile cooldown error counters before computing the next backoff so stale on-disk counters do not re-escalate into long cooldown loops after expiry. ([#41028](https://github.com/openclaw/openclaw/pull/41028)) thanks [@zerone0x](https://github.com/zerone0x).
  * Agents/memory flush: forward `memoryFlushWritePath` through `runEmbeddedPiAgent` so memory-triggered flush turns keep the append-only write guard without aborting before tool setup. Follows up on [#38574](https://github.com/openclaw/openclaw/pull/38574). ([#41761](https://github.com/openclaw/openclaw/pull/41761)) Thanks [@frankekn](https://github.com/frankekn).
  * Agents/context pruning: prune image-only tool results during soft-trim, align context-pruning coverage with the new tool-result contract, and extend historical image cleanup to the same screenshot-heavy session path. ([#43045](https://github.com/openclaw/openclaw/pull/43045)) Thanks [@MoerAI](https://github.com/MoerAI).
  * Sessions/reset model recompute: clear stale runtime model, context-token, and system-prompt metadata before session resets recompute the replacement session, so resets pick up current defaults and explicit overrides instead of reusing old runtime model state. ([#41173](https://github.com/openclaw/openclaw/pull/41173)) thanks [@pon](https://github.com/pon)...

[Read more](https://github.com/openclaw/openclaw/releases/tag/v2026.3.11-beta.1)
### Contributors
  * [ ![@zeroasterisk](https://avatars.githubusercontent.com/u/23422?s=64&v=4) ](https://github.com/zeroasterisk)
  * [ ![@vincentkoc](https://avatars.githubusercontent.com/u/25068?s=64&v=4) ](https://github.com/vincentkoc)
  * [ ![@velvet-shark](https://avatars.githubusercontent.com/u/126378?s=64&v=4) ](https://github.com/velvet-shark)
  * [ ![@davidguttman](https://avatars.githubusercontent.com/u/431696?s=64&v=4) ](https://github.com/davidguttman)
  * [ ![@mvanhorn](https://avatars.githubusercontent.com/u/455140?s=64&v=4) ](https://github.com/mvanhorn)
  * [ ![@pejmanjohn](https://avatars.githubusercontent.com/u/481729?s=64&v=4) ](https://github.com/pejmanjohn)
  * [ ![@xinhuagu](https://avatars.githubusercontent.com/u/562450?s=64&v=4) ](https://github.com/xinhuagu)
  * [ ![@joshavant](https://avatars.githubusercontent.com/u/830519?s=64&v=4) ](https://github.com/joshavant)
  * [ ![@kyohwang](https://avatars.githubusercontent.com/u/1436387?s=64&v=4) ](https://github.com/kyohwang)
  * [ ![@ngutman](https://avatars.githubusercontent.com/u/1540134?s=64&v=4) ](https://github.com/ngutman)
  * [ ![@imwyvern](https://avatars.githubusercontent.com/u/1765672?s=64&v=4) ](https://github.com/imwyvern)
  * [ ![@andyliu](https://avatars.githubusercontent.com/u/2377291?s=64&v=4) ](https://github.com/andyliu)
  * [ ![@hnykda](https://avatars.githubusercontent.com/u/2741256?s=64&v=4) ](https://github.com/hnykda)
  * [ ![@BradGroux](https://avatars.githubusercontent.com/u/3053586?s=64&v=4) ](https://github.com/BradGroux)
  * [ ![@jackal092927](https://avatars.githubusercontent.com/u/3854860?s=64&v=4) ](https://github.com/jackal092927)
  * [ ![@sircrumpet](https://avatars.githubusercontent.com/u/4436535?s=64&v=4) ](https://github.com/sircrumpet)
  * [ ![@frankekn](https://avatars.githubusercontent.com/u/4488090?s=64&v=4) ](https://github.com/frankekn)
  * [ ![@ademczuk](https://avatars.githubusercontent.com/u/5212682?s=64&v=4) ](https://github.com/ademczuk)
  * [ ![@gumadeiras](https://avatars.githubusercontent.com/u/5599352?s=64&v=4) ](https://github.com/gumadeiras)
  * [ ![@huntharo](https://avatars.githubusercontent.com/u/5617868?s=64&v=4) ](https://github.com/huntharo)
  * [ ![@BruceMacD](https://avatars.githubusercontent.com/u/5853428?s=64&v=4) ](https://github.com/BruceMacD)
  * [ ![@ingyukoh](https://avatars.githubusercontent.com/u/6015960?s=64&v=4) ](https://github.com/ingyukoh)
  * [ ![@rbutera](https://avatars.githubusercontent.com/u/6047293?s=64&v=4) ](https://github.com/rbutera)
  * [ ![@tdjackey](https://avatars.githubusercontent.com/u/6791132?s=64&v=4) ](https://github.com/tdjackey)
  * [ ![@altaywtf](https://avatars.githubusercontent.com/u/9790196?s=64&v=4) ](https://github.com/altaywtf)
  * [ ![@pomelo-nwu](https://avatars.githubusercontent.com/u/10703060?s=64&v=4) ](https://github.com/pomelo-nwu)
  * [ ![@benjipeng](https://avatars.githubusercontent.com/u/11394934?s=64&v=4) ](https://github.com/benjipeng)
  * [ ![@jnMetaCode](https://avatars.githubusercontent.com/u/12096460?s=64&v=4) ](https://github.com/jnMetaCode)
  * [ ![@BillChirico](https://avatars.githubusercontent.com/u/13951316?s=64&v=4) ](https://github.com/BillChirico)
  * [ ![@zheliu2](https://avatars.githubusercontent.com/u/15888718?s=64&v=4) ](https://github.com/zheliu2)
  * [ ![@jiarung](https://avatars.githubusercontent.com/u/16461359?s=64&v=4) ](https://github.com/jiarung)
  * [ ![@obviyus](https://avatars.githubusercontent.com/u/22031114?s=64&v=4) ](https://github.com/obviyus)
  * [ ![@MoerAI](https://avatars.githubusercontent.com/u/26067127?s=64&v=4) ](https://github.com/MoerAI)
  * [ ![@CryUshio](https://avatars.githubusercontent.com/u/30655354?s=64&v=4) ](https://github.com/CryUshio)
  * [ ![@urianpaul94](https://avatars.githubusercontent.com/u/33277984?s=64&v=4) ](https://github.com/urianpaul94)
  * [ ![@zhoulf1006](https://avatars.githubusercontent.com/u/35586967?s=64&v=4) ](https://github.com/zhoulf1006)
  * [ ![@cgdusek](https://avatars.githubusercontent.com/u/38732970?s=64&v=4) ](https://github.com/cgdusek)
  * [ ![@zerone0x](https://avatars.githubusercontent.com/u/39543393?s=64&v=4) ](https://github.com/zerone0x)
  * [ ![@ayanesakura](https://avatars.githubusercontent.com/u/40628300?s=64&v=4) ](https://github.com/ayanesakura)
  * [ ![@ApacheBin](https://avatars.githubusercontent.com/u/43498191?s=64&v=4) ](https://github.com/ApacheBin)
  * [ ![@davidrudduck](https://avatars.githubusercontent.com/u/47308254?s=64&v=4) ](https://github.com/davidrudduck)
  * [ ![@opriz](https://avatars.githubusercontent.com/u/51957849?s=64&v=4) ](https://github.com/opriz)
  * [ ![@VibhorGautam](https://avatars.githubusercontent.com/u/55019395?s=64&v=4) ](https://github.com/VibhorGautam)
  * [ ![@BunsDev](https://avatars.githubusercontent.com/u/68980965?s=64&v=4) ](https://github.com/BunsDev)
  * [ ![@ping-Toven](https://avatars.githubusercontent.com/u/69218856?s=64&v=4) ](https://github.com/ping-Toven)
  * [ ![@Julbarth](https://avatars.githubusercontent.com/u/72460857?s=64&v=4) ](https://github.com/Julbarth)
  * [ ![@laurieluo](https://avatars.githubusercontent.com/u/89195476?s=64&v=4) ](https://github.com/laurieluo)
  * [ ![@ImLukeF](https://avatars.githubusercontent.com/u/92253590?s=64&v=4) ](https://github.com/ImLukeF)
  * [ ![@hougangdev](https://avatars.githubusercontent.com/u/105773686?s=64&v=4) ](https://github.com/hougangdev)
  * [ ![@Jimmy-xuzimo](https://avatars.githubusercontent.com/u/111618279?s=64&v=4) ](https://github.com/Jimmy-xuzimo)
  * [ ![@mbelinky](https://avatars.githubusercontent.com/u/132747814?s=64&v=4) ](https://github.com/mbelinky)
  * [ ![@Squabble9](https://avatars.githubusercontent.com/u/194720422?s=64&v=4) ](https://github.com/Squabble9)
  * [ ![@smysle](https://avatars.githubusercontent.com/u/207193754?s=64&v=4) ](https://github.com/smysle)
  * [ ![@dsantoreis](https://avatars.githubusercontent.com/u/220753637?s=64&v=4) ](https://github.com/dsantoreis)
  * [ ![@futuremind2026](https://avatars.githubusercontent.com/u/258860756?s=64&v=4) ](https://github.com/futuremind2026)
  * [ ![@echo931](https://avatars.githubusercontent.com/u/259437483?s=64&v=4) ](https://github.com/echo931)
  * [ ![@dutifulbob](https://avatars.githubusercontent.com/u/261991368?s=64&v=4) ](https://github.com/dutifulbob)
  * [ ![@xaeon2026](https://avatars.githubusercontent.com/u/264572156?s=64&v=4) ](https://github.com/xaeon2026)
  * [ ![@PonyX-lab](https://avatars.githubusercontent.com/u/266766228?s=64&v=4) ](https://github.com/PonyX-lab)

zeroasterisk, vincentkoc, and 57 other contributors
Assets 3
Loading
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
👍 3 egoan82, ParamThakkar123, and yasir-shahhhhh reacted with thumbs up emoji 🎉 11 viandikafauzi, ysansan98, kasnol, madhavsomani, sibbl, alanxchen85, GosuDRM, Tony3-user, ParamThakkar123, Apartman36, and wanyuxue12 reacted with hooray emoji 🚀 1 chib30333 reacted with rocket emoji 👀 4 jiahanglou1117-cpu, egoan82, ParamThakkar123, and mrverdant13 reacted with eyes emoji
All reactions
  * 👍 3 reactions
  * 🎉 11 reactions
  * 🚀 1 reaction
  * 👀 4 reactions

16 people reacted
## openclaw 2026.3.8
09 Mar 07:49
![@steipete](https://avatars.githubusercontent.com/u/58493?s=40&v=4) [steipete](https://github.com/steipete)
Immutable release. Only release title and notes can be modified.
[ v2026.3.8  ](https://github.com/openclaw/openclaw/tree/v2026.3.8)
[ `3caab92`](https://github.com/openclaw/openclaw/commit/3caab9260cb0a0064e6a37b2de3bedc8a547e599)
Compare
#  Choose a tag to compare
## Sorry, something went wrong.
Filter
Loading
## Sorry, something went wrong.
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
## No results found
[View all tags](https://github.com/openclaw/openclaw/tags)
[openclaw 2026.3.8](https://github.com/openclaw/openclaw/releases/tag/v2026.3.8)
Mac assets on this release reuse the beta artifact line from v2026.3.8-beta.1.
### Changes
  * CLI/backup: add `openclaw backup create` and `openclaw backup verify` for local state archives, including `--only-config`, `--no-include-workspace`, manifest/payload validation, and backup guidance in destructive flows. ([#40163](https://github.com/openclaw/openclaw/pull/40163)) thanks [@shichangs](https://github.com/shichangs).
  * macOS/onboarding: add a remote gateway token field for remote mode, preserve existing non-plaintext `gateway.remote.token` config values until explicitly replaced, and warn when the loaded token shape cannot be used directly from the macOS app. ([#40187](https://github.com/openclaw/openclaw/pull/40187), supersedes [#34614](https://github.com/openclaw/openclaw/pull/34614)) Thanks [@cgdusek](https://github.com/cgdusek).
  * Talk mode: add top-level `talk.silenceTimeoutMs` config so Talk waits a configurable amount of silence before auto-sending the current transcript, while keeping each platform's existing default pause window when unset. ([#39607](https://github.com/openclaw/openclaw/pull/39607)) Thanks [@danodoesdesign](https://github.com/danodoesdesign). Fixes [#17147](https://github.com/openclaw/openclaw/issues/17147).
  * TUI: infer the active agent from the current workspace when launched inside a configured agent workspace, while preserving explicit `agent:` session targets. ([#39591](https://github.com/openclaw/openclaw/pull/39591)) thanks [@arceus77-7](https://github.com/arceus77-7).
  * Tools/Brave web search: add opt-in `tools.web.search.brave.mode: "llm-context"` so `web_search` can call Brave's LLM Context endpoint and return extracted grounding snippets with source metadata, plus config/docs/test coverage. ([#33383](https://github.com/openclaw/openclaw/pull/33383)) Thanks [@thirumaleshp](https://github.com/thirumaleshp).
  * CLI/install: include the short git commit hash in `openclaw --version` output when metadata is available, and keep installer version checks compatible with the decorated format. ([#39712](https://github.com/openclaw/openclaw/pull/39712)) thanks [@sourman](https://github.com/sourman).
  * CLI/backup: improve archive naming for date sorting, add config-only backup mode, and harden backup planning, publication, and verification edge cases. ([#40163](https://github.com/openclaw/openclaw/pull/40163)) Thanks [@gumadeiras](https://github.com/gumadeiras).
  * ACP/Provenance: add optional ACP ingress provenance metadata and visible receipt injection (`openclaw acp --provenance off|meta|meta+receipt`) so OpenClaw agents can retain and report ACP-origin context with session trace IDs. ([#40473](https://github.com/openclaw/openclaw/pull/40473)) thanks [@mbelinky](https://github.com/mbelinky).
  * Tools/web search: alphabetize provider ordering across runtime selection, onboarding/configure pickers, and config metadata, so provider lists stay neutral and multi-key auto-detect now prefers Grok before Kimi. ([#40259](https://github.com/openclaw/openclaw/pull/40259)) thanks [@kesku](https://github.com/kesku).
  * Docs/Web search: restore $5/month free-credit details, replace defunct "Data for Search"/"Data for AI" plan names with current "Search" plan, and note legacy subscription validity in Brave setup docs. Follows up on [#26860](https://github.com/openclaw/openclaw/pull/26860). ([#40111](https://github.com/openclaw/openclaw/pull/40111)) Thanks [@remusao](https://github.com/remusao).
  * Extensions/ACPX tests: move the shared runtime fixture helper from `src/runtime-internals/` to `src/test-utils/` so the test-only helper no longer looks like shipped runtime code.

### Fixes
  * Update/macOS launchd restart: re-enable disabled LaunchAgent services before updater bootstrap so `openclaw update` can recover from a disabled gateway service instead of leaving the restart step stuck.
  * macOS app/chat UI: route browser proxy through the local node browser service, preserve plain-text paste semantics, strip completed assistant trace/debug wrapper noise from transcripts, refresh permission state after returning from System Settings, and tolerate malformed cron rows in the macOS tab. ([#39516](https://github.com/openclaw/openclaw/pull/39516)) Thanks @Imhermes1.
  * Android/Play distribution: remove self-update, background location, `screen.record`, and background mic capture from the Android app, narrow the foreground service to `dataSync` only, and clean up the legacy `location.enabledMode=always` preference migration. ([#39660](https://github.com/openclaw/openclaw/pull/39660)) Thanks [@obviyus](https://github.com/obviyus).
  * Telegram/DM routing: dedupe inbound Telegram DMs per agent instead of per session key so the same DM cannot trigger duplicate replies when both `agent:main:main` and `agent:main:telegram:direct:<id>` resolve for one agent. Fixes [#40005](https://github.com/openclaw/openclaw/issues/40005). Supersedes [#40116](https://github.com/openclaw/openclaw/pull/40116). ([#40519](https://github.com/openclaw/openclaw/pull/40519)) thanks [@obviyus](https://github.com/obviyus).
  * Cron/Telegram announce delivery: route text-only announce jobs through the real outbound adapters after finalizing descendant output so plain Telegram targets no longer report `delivered: true` when no message actually reached Telegram. ([#40575](https://github.com/openclaw/openclaw/pull/40575)) thanks [@obviyus](https://github.com/obviyus).
  * Matrix/DM routing: add safer fallback detection for broken `m.direct` homeservers, honor explicit room bindings over DM classification, and preserve room-bound agent selection for Matrix DM rooms. ([#19736](https://github.com/openclaw/openclaw/pull/19736)) Thanks [@derbronko](https://github.com/derbronko).
  * Feishu/plugin onboarding: clear the short-lived plugin discovery cache before reloading the registry after installing a channel plugin, so onboarding no longer re-prompts to download Feishu immediately after a successful install. Fixes [#39642](https://github.com/openclaw/openclaw/issues/39642). ([#39752](https://github.com/openclaw/openclaw/pull/39752)) Thanks [@GazeKingNuWu](https://github.com/GazeKingNuWu).
  * Plugins/channel onboarding: prefer bundled channel plugins over duplicate npm-installed copies during onboarding and release-channel sync, preventing bundled plugins from being shadowed by npm installs with the same plugin ID. ([#40092](https://github.com/openclaw/openclaw/issues/40092))
  * Config/runtime snapshots: keep secrets-runtime-resolved config and auth-profile snapshots intact after config writes so follow-up reads still see file-backed secret values while picking up the persisted config update. ([#37313](https://github.com/openclaw/openclaw/pull/37313)) thanks [@bbblending](https://github.com/bbblending).
  * Gateway/Control UI: resolve bundled dashboard assets through symlinked global wrappers and auto-detected package roots, while keeping configured and custom roots on the strict hardlink boundary. ([#40385](https://github.com/openclaw/openclaw/pull/40385)) Thanks [@LarytheLord](https://github.com/LarytheLord).
  * Browser/extension relay: add `browser.relayBindHost` so the Chrome relay can bind to an explicit non-loopback address for WSL2 and other cross-namespace setups, while preserving loopback-only defaults. ([#39364](https://github.com/openclaw/openclaw/pull/39364)) Thanks [@mvanhorn](https://github.com/mvanhorn).
  * Browser/CDP: normalize loopback direct WebSocket CDP URLs back to HTTP(S) for `/json/*` tab operations so local `ws://` / `wss://` profiles can still list, focus, open, and close tabs after the new direct-WS support lands. ([#31085](https://github.com/openclaw/openclaw/pull/31085)) Thanks [@shrey150](https://github.com/shrey150).
  * Browser/CDP: rewrite wildcard `ws://0.0.0.0` and `ws://[::]` debugger URLs from remote `/json/version` responses back to the external CDP host/port, fixing Browserless-style container endpoints. ([#17760](https://github.com/openclaw/openclaw/pull/17760)) Thanks [@joeharouni](https://github.com/joeharouni).
  * Browser/extension relay: wait briefly for a previously attached Chrome tab to reappear after transient relay drops before failing with `tab not found`, reducing noisy reconnect flakes. ([#32461](https://github.com/openclaw/openclaw/pull/32461)) Thanks [@AaronWander](https://github.com/AaronWander).
  * macOS/Tailscale gateway discovery: keep Tailscale Serve probing alive when other remote gateways are already discovered, prefer direct transport for resolved `.ts.net` and Tailscale Serve gateways, and set `TERM=dumb` for GUI-launched Tailscale CLI discovery. ([#40167](https://github.com/openclaw/openclaw/pull/40167)) thanks [@ngutman](https://github.com/ngutman).
  * TUI/theme: detect light terminal backgrounds via `COLORFGBG` and pick a WCAG AA-compliant light palette, with `OPENCLAW_THEME=light|dark` override for terminals without auto-detection. ([#38636](https://github.com/openclaw/openclaw/pull/38636)) Thanks [@ademczuk](https://github.com/ademczuk) and [@vincentkoc](https://github.com/vincentkoc).
  * Agents/openai-codex: normalize `gpt-5.4` fallback transport back to `openai-codex-responses` on `chatgpt.com/backend-api` when config drifts to the generic OpenAI responses endpoint. ([#38736](https://github.com/openclaw/openclaw/pull/38736)) Thanks [@0xsline](https://github.com/0xsline).
  * Models/openai-codex GPT-5.4 forward-compat: use the GPT-5.4 1,050,000-token context window and 128,000 max tokens for `openai-codex/gpt-5.4` instead of inheriting stale legacy Codex limits in resolver fallbacks and model listing. ([#37876](https://github.com/openclaw/openclaw/pull/37876)) thanks [@yuweuii](https://github.com/yuweuii).
  * Tools/web search: restore Perplexity OpenRouter/Sonar compatibility for legacy `OPENROUTER_API_KEY`, `sk-or-...`, and explicit `perplexity.baseUrl` / `model` setups while keeping direct Perplexity keys on the native Search API path. ([#39937](https://github.com/openclaw/openclaw/pull/39937)) Thanks [@obviyus](https://github.com/obviyus).
  * Agents/failover: detect Amazon Bedrock `Too many tokens per day` quota errors as rate limits across fallback, cron retry, and memory embeddings while keeping context-window `too many tokens per request` errors out of the rate-limit lane. ([#39377](https://github.com/openclaw/openclaw/pull/39377)) Thanks [@gambletan](https://github.com/gambletan).
  * Mattermost replies: keep `root_id` pinned to the existing thread root when an agent replies inside a thread, while still using reply-target threading for top-level posts. ([#27744](https://github.com/openclaw/openclaw/pull/27744)) thanks [@hnykda](https://github.com/hnykda).
  * Telegram/DM partial streaming: keep DM preview lanes on real message edits instead of native draft materialization so final replies no longer flash a second duplicate copy before collapsing back to one.
  * macOS overlays: fix VoiceWake, Talk, and Notify overlay exclusivity crashes by removing shared `inout` visibility mutation from `OverlayPanelFactory.present`, and add a repeated Talk overlay smoke test. ([#39275](https://github.com/openclaw/openclaw/issues/39275), [#39321](https://github.com/openclaw/openclaw/pull/39321)) Thanks [@fellanH](https://github.com/fellanH).
  * macOS Talk Mode: set the speech recognition request `taskHint` to `.dictation` for mic capture, and add regression coverage for the request defaults. ([#38445](https://github.com/openclaw/openclaw/pull/38445)) Thanks [@dmiv](https://github.com/dmiv).
  * macOS release packaging: default `scripts/package-mac-app.sh` to universal binaries for `BUILD_CONFIG=release`, and clarify that `scripts/package-mac-dist.sh` already produces the release zip + DMG. ([#33891](https://github.com/openclaw/openclaw/pull/33891)) Thanks [@cgdusek](https://github.com/cgdusek).
  * Hooks/session-memory: keep `/new` and `/reset` memory artifacts in the bound agent workspace and align saved reset session keys with that workspace when stale main-agent keys leak into the hook path. ([#39875](https://github.com/openclaw/openclaw/pull/39875)) thanks [@rbutera](https://github.com/rbutera).
  * Sessions/model switch: clear stale cached `contextTokens` when a session changes models so status and runtime paths recompute against the active model window. ([#38044](https://github.com/openclaw/openclaw/pull/38044)) thanks [@yuweuii](https://github.com/yuweuii).
  * ACP/session history: persist transcripts for successful ACP child runs, preserve exact transcript text, record ACP spawned-session lineage, and keep spawn-time transcript-path persistence best-effort so history storage failures do not block execution. ([#40137](https://github.com/openclaw/openclaw/pull/40137)) thanks [@mbelinky](https://github.com/mbelinky).
  * Docs/browser: add a layered WSL2 + Windows remote Chrome CDP troubleshooting guide, including Control UI origin pitfalls and extension-relay bind-address guidance. ([#39407](https://github.com/openclaw/openclaw/pull/39407)) Thanks [@Owlock](https://github.com/Owlock).
  * Context engine registry/bundled builds: share the registry state through a `globalThis` singleton so duplicated bundled module copies can resolve engines registered by each other at runtime, with regression coverage for duplicate-module imports. ([#40115](https://github.com/openclaw/openclaw/pull/40115)) thanks [@jalehman](https://github.com/jalehman).
  * Podman/setup: fix `cannot chdir: Permission denied` in `run_as_user` when `...

[Read more](https://github.com/openclaw/openclaw/releases/tag/v2026.3.8)
### Contributors
  * [ ![@vincentkoc](https://avatars.githubusercontent.com/u/25068?s=64&v=4) ](https://github.com/vincentkoc)
  * [ ![@velvet-shark](https://avatars.githubusercontent.com/u/126378?s=64&v=4) ](https://github.com/velvet-shark)
  * [ ![@mvanhorn](https://avatars.githubusercontent.com/u/455140?s=64&v=4) ](https://github.com/mvanhorn)
  * [ ![@jalehman](https://avatars.githubusercontent.com/u/550978?s=64&v=4) ](https://github.com/jalehman)
  * [ ![@zpbrent](https://avatars.githubusercontent.com/u/834641?s=64&v=4) ](https://github.com/zpbrent)
  * [ ![@dimat](https://avatars.githubusercontent.com/u/1256209?s=64&v=4) ](https://github.com/dimat)
  * [ ![@remusao](https://avatars.githubusercontent.com/u/1299873?s=64&v=4) ](https://github.com/remusao)
  * [ ![@ngutman](https://avatars.githubusercontent.com/u/1540134?s=64&v=4) ](https://github.com/ngutman)
  * [ ![@langdon](https://avatars.githubusercontent.com/u/1832177?s=64&v=4) ](https://github.com/langdon)
  * [ ![@derbronko](https://avatars.githubusercontent.com/u/2217509?s=64&v=4) ](https://github.com/derbronko)
  * [ ![@hnykda](https://avatars.githubusercontent.com/u/2741256?s=64&v=4) ](https://github.com/hnykda)
  * [ ![@shrey150](https://avatars.githubusercontent.com/u/3813908?s=64&v=4) ](https://github.com/shrey150)
  * [ ![@sourman](https://avatars.githubusercontent.com/u/3827766?s=64&v=4) ](https://github.com/sourman)
  * [ ![@jlcbk](https://avatars.githubusercontent.com/u/4089745?s=64&v=4) ](https://github.com/jlcbk)
  * [ ![@ademczuk](https://avatars.githubusercontent.com/u/5212682?s=64&v=4) ](https://github.com/ademczuk)
  * [ ![@gumadeiras](https://avatars.githubusercontent.com/u/5599352?s=64&v=4) ](https://github.com/gumadeiras)
  * [ ![@rbutera](https://avatars.githubusercontent.com/u/6047293?s=64&v=4) ](https://github.com/rbutera)
  * [ ![@rexlunae](https://avatars.githubusercontent.com/u/6726134?s=64&v=4) ](https://github.com/rexlunae)
  * [ ![@tdjackey](https://avatars.githubusercontent.com/u/6791132?s=64&v=4) ](https://github.com/tdjackey)
  * [ ![@dmiv](https://avatars.githubusercontent.com/u/8742027?s=64&v=4) ](https://github.com/dmiv)
  * [ ![@joeharouni](https://avatars.githubusercontent.com/u/11054404?s=64&v=4) ](https://github.com/joeharouni)
  * [ ![@obviyus](https://avatars.githubusercontent.com/u/22031114?s=64&v=4) ](https://github.com/obviyus)
  * [ ![@fellanH](https://avatars.githubusercontent.com/u/30758862?s=64&v=4) ](https://github.com/fellanH)
  * [ ![@cgdusek](https://avatars.githubusercontent.com/u/38732970?s=64&v=4) ](https://github.com/cgdusek)
  * [ ![@lml2468](https://avatars.githubusercontent.com/u/39320777?s=64&v=4) ](https://github.com/lml2468)
  * [ ![@tysoncung](https://avatars.githubusercontent.com/u/45380903?s=64&v=4) ](https://github.com/tysoncung)
  * [ ![@shichangs](https://avatars.githubusercontent.com/u/46870204?s=64&v=4) ](https://github.com/shichangs)
  * [ ![@kesku](https://avatars.githubusercontent.com/u/62210496?s=64&v=4) ](https://github.com/kesku)
  * [ ![@danodoesdesign](https://avatars.githubusercontent.com/u/63997706?s=64&v=4) ](https://github.com/danodoesdesign)
  * [ ![@yuweuii](https://avatars.githubusercontent.com/u/82372187?s=64&v=4) ](https://github.com/yuweuii)
  * [ ![@thirumaleshp](https://avatars.githubusercontent.com/u/85149081?s=64&v=4) ](https://github.com/thirumaleshp)
  * [ ![@bbblending](https://avatars.githubusercontent.com/u/122739024?s=64&v=4) ](https://github.com/bbblending)
  * [ ![@githubbzxs](https://avatars.githubusercontent.com/u/123316733?s=64&v=4) ](https://github.com/githubbzxs)
  * [ ![@mbelinky](https://avatars.githubusercontent.com/u/132747814?s=64&v=4) ](https://github.com/mbelinky)
  * [ ![@Owlock](https://avatars.githubusercontent.com/u/135854806?s=64&v=4) ](https://github.com/Owlock)
  * [ ![@0xsline](https://avatars.githubusercontent.com/u/151105947?s=64&v=4) ](https://github.com/0xsline)
  * [ ![@LarytheLord](https://avatars.githubusercontent.com/u/169234180?s=64&v=4) ](https://github.com/LarytheLord)
  * [ ![@Gkinthecodeland](https://avatars.githubusercontent.com/u/205207736?s=64&v=4) ](https://github.com/Gkinthecodeland)
  * [ ![@AaronWander](https://avatars.githubusercontent.com/u/210468848?s=64&v=4) ](https://github.com/AaronWander)
  * [ ![@dsantoreis](https://avatars.githubusercontent.com/u/220753637?s=64&v=4) ](https://github.com/dsantoreis)
  * [ ![@arceus77-7](https://avatars.githubusercontent.com/u/261276524?s=64&v=4) ](https://github.com/arceus77-7)
  * [ ![@GazeKingNuWu](https://avatars.githubusercontent.com/u/264914544?s=64&v=4) ](https://github.com/GazeKingNuWu)
  * [ ![@gambletan](https://avatars.githubusercontent.com/u/266203672?s=64&v=4) ](https://github.com/gambletan)

vincentkoc, velvet-shark, and 41 other contributors
Assets 6
Loading
###  Uh oh!
There was an error while loading. [Please reload this page](https://github.com/openclaw/openclaw/releases).
👍 210 ieshaalcina, nek1987, Itz-Murali, voytas75, echoyolo6, vgdh, naelyaasasafitri, Xinruyu54088, ngd-b, lyang8222, and 200 more reacted with thumbs up emoji 😄 21 Faisal-911M, orwiso, wuzguo, 1342204844-lang, birdofprey, coygeek, vixclotet, euclidesdry-tripee, JOrk23456, AlexMao97, and 11 more reacted with laugh emoji 🎉 35 ngd-b, Mushy-Snugglebites-badonkadonk, dorogoy, orwiso, Faisal-911M, gitabtion, IthaiT, Chemaclass, wuzguo, i-iooi-i, and 25 more reacted with hooray emoji ❤️ 38 orwiso, Faisal-911M, Chemaclass, wuzguo, i-iooi-i, nikhil8182, rainerdechet, niuwengang, hucklam, Laminua, and 28 more reacted with heart emoji 🚀 30 Mushy-Snugglebites-badonkadonk, rahul961004, orwiso, Faisal-911M, Chemaclass, wuzguo, i-iooi-i, Juvin-Chen, 1342204844-lang, birdofprey, and 20 more reacted with rocket emoji 👀 22 checkzhao8888, yougrandpa, Faisal-911M, orwiso, reclu3a, Puiching-Memory, urtzai, wuzguo, aswifi, Samuhaer98, and 12 more reacted with eyes emoji
All reactions
  * 👍 210 reactions
  * 😄 21 reactions
  * 🎉 35 reactions
  * ❤️ 38 reactions
  * 🚀 30 reactions
  * 👀 22 reactions

262 people reacted
## openclaw 2026.3.8-beta.1
09 Mar 07:19
![@steipete](https://avatars.githubusercontent.com/u/58493?s=40&v=4) [steipete](https://github.com/steipete)
Immutable release. On