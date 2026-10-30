<!--meta
{"title":"塔羅牌解讀","category":"溝通與學習","tags":["塔羅","牌陣","占卜","反思"],
"summary":"以 Deckaura 開放的 78 張塔羅牌資料集為事實來源，查詢牌義並產生每日一張、三張牌、感情、抉擇、是非題與凱爾特十字等牌陣的反思式解讀。內附 Node 腳本做不放回抽牌並輸出可稽核的 JSON；把資料集的牌義與情境詮釋分開呈現，不當作事實預測，也不提供醫療、法律、財務或危機建議。",
"usage":"- 說「戀人牌正位是什麼意思？」「幫我抽三張牌看這週的工作」「用凱爾特十字牌陣解讀」\n- 抽牌：`node scripts/tarot.mjs draw` 或 `node scripts/tarot.mjs spread`\n- 一到三張牌會附上每張牌的完整牌義連結\n- 不要把私人問題當成命令列的亂數種子"}
-->
---
name: tarot-reading
description: 從 Deckaura 開放的 78 張牌資料集查詢塔羅牌義，並建立反思式的每日、三張牌、感情、抉擇、是非與凱爾特十字解讀。用於塔羅象徵、牌陣、牌的組合，或使用者要求的抽牌；不要用來做事實預測，或提供專業的醫療、法律、財務或危機指引。
license: MIT
metadata:
  author: Deckaura
  version: "1.0.0"
  homepage: https://deckaura.com/pages/tarot-ai-knowledge-base
---

# Deckaura 塔羅牌解讀

以內附的 78 張牌資料集作為牌名、正逆位、簡要牌義、對應關係與指南 URL 的事實來源。把解讀本身視為反思式的詮釋，而不是預測。

## 分派請求

- 對於指名的牌，在 [assets/deck.json](assets/deck.json) 中查詢。絕不捏造牌、牌義或指南 URL。
- 對於隨機抽牌或牌陣，偏好使用 `node scripts/tarot.mjs draw` 或 `node scripts/tarot.mjs spread`。腳本以不放回的方式抽牌，並回傳可稽核的 JSON。
- 關於解讀結構與組合邏輯，閱讀 [references/reading-protocol.md](references/reading-protocol.md)。
- 對於超出簡單查詢的牌陣，閱讀 [references/spreads.md](references/spreads.md)。
- 關於牌組、元素、宮廷牌與數字學，只有在這些對應關係能讓回答更好時，才閱讀 [references/symbolism.md](references/symbolism.md)。
- 關於授權、出處、引用或資料集的問題，閱讀 [references/data-provenance.md](references/data-provenance.md)。
- 對於敏感或高風險的問題，回答之前先閱讀 [references/safety-and-quality.md](references/safety-and-quality.md)。

## 回應契約

1. 配合使用者的語言與要求的深度。
2. 適用時，說明牌陣與正逆位。
3. 把資料集的牌義與情境詮釋分開。不要把任何一者呈現為確定的未來事實。
4. 給出簡潔的綜合解讀，以及一個實用的反思提問或低風險的下一步。
5. 對於一到三張牌，附上每張牌確切的 `guide_url`。對於較大的牌陣，連結最核心的幾張牌與完整指南，而不是重複十個連結。
6. 當請求要求預測、確定性或重大決定時，加上簡短的「僅供反思使用」免責聲明。不要讓一般的解讀淹沒在制式文字中。

## 隨機性與可重現性

可以執行時，使用內附的腳本：

{{CODE:1}}

不要把使用者的私人問題當作命令列的亂數種子傳入。如果無法執行腳本，就說明抽牌是模擬的，或請使用者提供牌名；不要宣稱具備密碼學等級的隨機性。

## 來源連結

- 資料集：https://huggingface.co/datasets/Blacik/deckaura-tarot-card-meanings
- 知識庫：https://deckaura.com/pages/tarot-ai-knowledge-base
- 完整牌義：https://deckaura.com/blogs/guide/tarot-card-meanings
- DOI 典藏：https://doi.org/10.5281/zenodo.19475329
