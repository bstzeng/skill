<!--meta
{"title":"去除 AI 腔的文字潤稿","category":"社群行銷","tags":["寫作","潤稿","去 AI 味","英文寫作","語氣保留"],
"summary":"一個範圍很窄的校稿技能：從既有的（英文）草稿中移除常見的機器寫作痕跡——濫用的詞彙（crucial、delve、seamless…）、誇大重要性的句子、空洞的權威引述、句尾的 -ing 尾巴、「不只 X 而是 Y」、湊三項的清單、粗體小標清單、助理腔、假洞見的鋪陳等 24 類模式，同時完全不改變內容與作者語氣。每項規則分為直接修（FIX）、只標記（FLAG）與先問（ASK）三級；也有只偵測不修改的模式。",
"usage":"- 貼上草稿說「幫我去掉 AI 味，但保留我的語氣」\n- 只想檢查時說「幫我掃描這篇哪裡像 AI 寫的，不要改」\n- 有專案語氣設定檔時會先讀；可用 `references/voice-profile-template.md` 建立\n- 只編輯你有權修改的既有文字，不負責從零撰寫，也不判定他人文章是否為 AI 所寫\n- 規則主要針對英文文字"}
-->
---
name: human-writer
description: 你的草稿常常讀起來平淡、重複又過度修飾，而且經常偏離作者原本的意圖。本技能清理機器式的措辭、移除機器寫作的套路，並讓文字更順暢，同時完全保留你自然的語氣與訊息。
license: MIT
metadata:
  version: 1.2.0
---

# Human Writer：保留自然語氣的編修

本技能的工作很窄：從既有的草稿中移除常見的機器寫作模式，而不改變它的意思，也不把作者的語氣磨平。它是一輪專門的校稿，不是共同寫作。

## 凌駕一切的唯一規則

**不要增加、刪除或改變作者所寫內容的實質。** 不加新的主張、例子、意見、細微差別，也不補空缺。不要「改善」論點。如果一個句子簡短而直接，它就維持簡短而直接。如果一個段落沒寫完或很隨性，它就維持那樣，除非唯一的問題是裡面有機器寫作的模式。

例外只有兩個，就只有這兩個：
1. **事實錯誤：** 客觀上錯誤的日期、名字、數字或主張。標記出來，並在修改之前先詢問。不要默默「修正」你無法驗證的事實。
2. **必要的修補：** 移除某個模式後句子結構壞掉，需要最小限度的修補才能維持合乎文法。只修補移除動作弄壞的部分。

如果你不確定某個修改是否已從「移除模式」越界到「改寫作者」，就不要改。保留那一行並標記它。

## 動作等級

下方每個檢查項目都帶有三種動作之一。絕不要把 FLAG 項目升級成自動修正。

- **FIX（修）：** 默默套用最小的修正，例如換一個字、改標點或刪除一個子句。
- **FLAG（標記）：** 保留原文，並在備註中列出。用於這個模式有可能確實是作者刻意選擇的情況。
- **ASK（問）：** 在碰觸事實錯誤之前，停下來確認。

## 語氣設定檔

目標永遠不是「一般的人類」。保留所提供之作者的語氣。如果有專案語氣設定檔，在編修前先閱讀並遵循。建立設定檔時使用 `references/voice-profile-template.md`。如果沒有設定檔，只推斷草稿中可見的特徵，並以最輕的方式處理。

- **標點：** 遵循任何專案規則。如果沒有規則，不要加入長破折號。偏好能保留作者節奏的標點。
- **直接程度：** 如果一個修正可以更平實或更花俏，選更平實的。
- **術語與名稱：** 保留專案設定檔中核准的產品名稱、拼寫、大小寫與公開用語規則。

當要求的語域、編修深度或回報格式不明確時，閱讀 `references/editing-decision-guide.md`。在進行大幅編修之前，或當草稿有獨特的個人語氣時，閱讀 `references/voice-preservation-checklist.md`。對於面向大眾的檔案編修，在交回之前對完成的檔案執行 `scripts/check_editorial_rules.py`。只有在作者要求為一次長篇編修附上正式的修訂說明時，才使用 `assets/revision-note-template.md`。

## 兩種工作

**編修（預設）。** 作者提供一份要修的草稿。依照下方檢查清單做最小但有效的編修，並交回修正後的草稿。

**偵測。** 作者詢問一份草稿讀起來是否像機器寫的，或要求在不改動的情況下稽核、掃描或標記它。說出每一個出現的模式、引用那一行，並用幾個字說明修法。不要改寫、不要替草稿打分數，也不要宣稱它是某個模型寫的。被點名的模式是作者可以直接檢視的證據。

這是一個針對使用者有權編修之草稿的編輯工具。它不是鑑定作者身分的工具。

## 工作流程

1. 在動任何東西之前，先把整篇讀一遍。記下語域：社群或聊天、文件，或書信往來。如果語域不明確，預設用最輕的方式處理。
2. **在編修之前先記下語氣。** 找出讓這篇文字與眾不同的三到五個特徵：用字、直率程度、句子長度、幽默、插話，或修飾的程度。把這當作內部檢查。如果某個修正會磨掉其中一個特徵，那就是改寫。不要做。
3. 對於偵測請求：以唯讀方式跑過檢查清單，產出「兩種工作」中描述的發現報告，然後就停在那裡。
4. 對於編修請求：對照檢查清單看過整篇。每遇到一個命中，就套用最小的 FIX 或記錄 FLAG。能換一個字解決的，絕不改寫整個句子。
5. **對照 `eval.md` 自我檢查。** 在交回編修後的草稿之前，用本技能資料夾中 `eval.md` 的每一個問題檢查它。決定一次大幅修訂是否可以交回時，閱讀 `docs/revision-acceptance-guide.md`。如果任何檢查失敗，修正草稿並再檢查一次。這能抓到步驟 4 漏掉的東西：替換用的字本身就在禁用清單上、修補過的句子現在以 -ing 尾巴結尾、反射性打出的長破折號，或步驟 2 中某個語氣特徵被磨平了。
6. 以修正後的文字作為主要輸出。保留作者的格式，包括換行與大小寫，除非格式本身就是那個模式。對於以檔案交付的長篇文字，直接編輯檔案，而不是在聊天中貼上一大片文字。
7. 回報：
- 短篇（貼文、回覆、幾句話）：只給修正後的版本。
- 有實質編修的長篇：在結尾附上一行精簡摘要，列出移除的類別與大約的命中次數，而不是逐行差異。
- 任何 FLAG 或 ASK 項目：在文字之後附上簡短的條列清單，引用那一行並附一行理由。
8. 如果沒有任何項目觸發檢查清單，就直白地說：「這篇已經讀起來很乾淨，沒有做任何修改。」不要為了顯得有用而捏造編修。

## 檢查清單

### 1. 禁用詞彙：一見就 FIX

這些字在真正的人類寫作中統計上很少見，在 LLM 的輸出中卻很常見。換成更平實的同義字，或者如果那個子句只是填充，就整個刪掉。

`crucial`、`pivotal`、`vital`、`key`（作形容詞）、`robust`、`intricate`/`intricacies`、`delve`、`dive into`/`deep dive`、`boast`/`boasts`（意思是「有」）、`bolstered`、`garner`、`underscore`/`underscores`（作動詞）、`highlight`/`highlighting`（作動詞）、`showcase`/`showcasing`、`emphasizing`、`enhance`、`elevate`、`empower`、`unlock`、`unleash`、`harness`、`leverage`（作動詞）、`streamline`、`seamless`/`seamlessly`、`fostering`、`align with`、`interplay`、`landscape`（抽象義）、`realm`（抽象義）、`tapestry`（抽象義）、`navigate`（抽象義，「navigate the complexities」）、`ever-evolving`、`fast-paced`、`game-changer`/`game-changing`、`cutting-edge`、`state-of-the-art`、`transformative`、`revolutionize`、`innovative`（作填充）、`holistic`、`synergy`、`testament`、`valuable insights`、`actionable insights`、`enduring`、`meticulous`/`meticulously`、`groundbreaking`、`renowned`、`vibrant`、`rich`（作填充形容詞）、`nestled`、`in the heart of`、`diverse array`、`myriad`、`plethora`、`commitment to`、`plays a role in`、`serves as a testament/reminder`、`at the end of the day`、`in today's world/climate/era`。

把複雜的同義字換回人類實際會用的平實字：`authored`→wrote、`utilized`→used、`attempted`→tried、`relocated`→moved、`prior to`→before、`in order to`→to、`passed away`→died（除非語氣需要委婉）。

### 2. 誇大的重要性／傳承膨脹：FIX

刪掉唯一功能是膨脹主題重要性的句子：「marks a pivotal moment」「represents a significant shift」「underscores its enduring legacy」「contributes to the broader conversation about X」「sets the stage for」。如果這個句子除了「這很重要」之外沒有任何實際資訊，就刪掉。如果它把一個真實的事實包在膨脹的包裝裡，保留事實、拆掉包裝。

### 3. 罐頭式引述／知名度暗示：FIX

刪掉模糊的權威用語：「industry reports suggest」「experts argue」「observers have noted」、沒有引用來源的「studies show」、「has been featured in [媒體清單]」「maintains an active social media presence」與「independent coverage confirms」。如果作者引用的是真實而具體的東西，保留引用，移除泛泛的權威姿態。也刪掉當作填充的假範圍句型：沒有描述真實範圍的「from X to Y」。

### 4. 膚淺的「-ing」尾巴子句：FIX

以一個懸垂的現在分詞子句重述重要性的句子結尾：「...cementing its place in...」「...highlighting the importance of...」「...ensuring long-term success.」幾乎都可以刪掉而不損失資訊。刪掉尾巴，保留句子。

### 5. 迴避繫動詞：FIX

LLM 會把平實的「is/are/has」換成「serves as」「stands as」「functions as」「boasts」「features」「represents」「acts as」。把平實的動詞放回去：「X serves as the backbone of Y」→「X is the backbone of Y」。「The app boasts five tools」→「The app has five tools」。

### 6. 否定式對仗：第一個 FLAG，之後的 FIX

為了修辭上的力道而非真正的對比所使用的「Not just X, but Y」／「not only X but also Y」／「It's not X, it's Y」。一個真正符合作者語氣的例子可以保留。標記它。同一篇出現兩個以上：除了最有力的一個之外全部壓平，並且也標記那個留下來的。

### 7. 湊三項的填充：FIX

為了聽起來周全而反射性使用的三項清單（「faster, cleaner, and more reliable」），其中兩項講的是同一件事，或者一個字就夠了。修剪到實際為真的部分，而不是為了湊滿模式。疊加的成對形容詞（「clear and concise」「simple and effective」）也一樣，一個形容詞就能撐住時就只留一個。

### 8. 長破折號：遵循語氣設定檔

如果專案語氣設定檔禁用長破折號，就全部移除。依句子的節奏換成逗號、冒號、句號或括號。當作破折號使用的雙連字號（`--`）也要轉換。如果設定檔沒有禁用，也不要加入新的長破折號。

### 9. 堆疊轉折詞：FIX

段落中的句子反射性地以「Additionally」「Moreover」「Furthermore」「However」「That said」「Ultimately」開頭。一個真正的轉折沒問題。一連串的轉折就是破綻：刪掉連接詞，讓句子自己站著，不調整任何順序。

### 10. 標題的 Title Case：FIX

如果標題使用泛用的 Title Case（「Key Features And Benefits」）而作者其餘的作品沒有，就改成句首大寫。如果「X: Why Y Matters」這種冒號標題模式出現超過一次，也要標記。

### 11. 粗體過度使用／行內小標條列：FIX

任何每個項目都以粗體的 2–3 字小標加冒號開頭的清單（「**Speed:** ...」／「**Reliability:** ...」）。在聊天與社群情境中是很強的破綻。改成平實的散文或普通清單，除非內容確實是參考資料、結構有其存在的價值。

### 12. 協作助理式措辭：FIX

先前自動化處理留下的助理語氣：「I hope this helps!」「Let me know if you'd like more detail」「Would you like me to expand on this?」「Certainly!」「Of course!」與「Great question」。刪掉。這種語氣不屬於作者自己的信件或貼文。

### 13. 避險免責聲明與知識截止語：FIX

「As of my last update」「while specific details are limited」「it's important to note that」「it's worth noting/mentioning」與「generally speaking」：當它們是空洞的避險而不是真正的但書時就刪掉。真正的但書保留。清喉嚨的話拿掉。

### 14. 章節總結（「In conclusion...」）：FIX

只是重述已經說過的內容的結尾段落（「In summary, X shows that...」）。刪掉。讓文章在最後一個真正的論點上結束。

### 15. 把表情符號當格式：專業情境 FIX，社群情境 FLAG

在專業與文件情境中，裝飾每個標題或項目的表情符號（「🚀 Let's Connect!」「📌 Key facts」）是一種模式。拿掉。在社群貼文中，保留作者明顯刻意且節制放置的表情符號。即使在那裡，也要標記系統性地每行都有的表情符號。

### 16. Markdown 滲入非 Markdown 情境：FIX

在純文字目的地（聊天回覆、電子郵件內文、純文字文件）中散落的 `**粗體**`、`##` 標題或 `---` 分隔線，會被當成字面字元顯示。轉換成純文字的等價寫法或拿掉。

### 17. 排版殘留：FIX

容易漏看的貼上殘留：彎引號與直引號混用、不換行空格、不尋常的 Unicode 項目符號或連字號，以及在全文其他地方都用一個空格時，句號後出現兩個空格。悄悄地正規化。

### 18. 段落節奏一致：只 FLAG

如果每個段落的長度幾乎一樣，每個句子都落在同樣 15–25 字的區間，即使用字乾淨，讀起來也像機器打節拍。絕不要為了修正這點而重組結構。用一行備註標記它，讓作者自行決定是否要變化。

### 19. 誘導互動的結尾：只 FLAG

社群貼文的結尾，如「Who else has experienced this?」「Thoughts?」「Drop a comment below.」人類確實會寫這些，所以絕不要自動刪除。當結尾相對於貼文其餘部分顯得硬接上去時，FLAG。

### 20. 假洞見的鋪陳：FIX

「This is the part most people skip」「here's what nobody tells you」「the part everyone misses」「what most people get wrong」。這些把作者捧成掌握祕密知識的唯一專家，然後通常交出很普通的東西。刪掉鋪陳，讓主張自己站住。「The part everyone misses: distribution is the moat」變成「Distribution is the moat」。

### 21. 冒號揭曉：FIX

一個名詞片語、一個冒號，然後是小寫開頭的戲劇性揭曉：「The detail that makes it work: a separate agent grades it.」「The best part: it learns.」這是製造出來的戲劇感，不是真正的強調。改寫成平實的句子。冒號保留給真正的清單、標籤與引文，而不是假裝懸疑的停頓。

### 22. 修辭性鋪陳：FIX

「What if I told you...」「Think about it:」「Plot twist:」，以及自問自答的問答組（「Is this hard? Yes.」）。拿掉戲劇化的鋪陳，直接說出重點。

### 23. 假深刻的收尾句與戲劇化的片段：FIX

把一個平實的重點變成可愛比喻或丟麥克風式格言的最後一句「深刻」台詞。刪掉它，不要把它改寫成更好的比喻：以草稿中已有的最清楚、具體的句子作結。同一家族的還有：「X. And Y. And Z.」式的堆疊片段，以及「Not a X. Not a Y. A Z.」式的否定列舉（與上面的否定式對仗不同，這是三拍以上，而不是單一對比）。壓縮成一個說出真正內容的平實句子。

### 24. 機械式的句型重複：只 FLAG

與段落長度一致（#18）不同：這是同樣的*句型*一再重複，連續三個簡短有力的片段，或一個段落中每個句子都以同樣的結構開頭（主詞—動詞—受詞、主詞—動詞—受詞）。絕不要為了修正這點而重組結構。標記它，讓作者自行決定是否要變化。

## 語域校準

- **社群／聊天**：最輕的處理。保留作者隨性的節奏、縮寫、句子片段與直率。只修硬性的模式：禁用詞彙、禁用標點、否定式對仗、助理式措辭與排版殘留。不要把任何東西變正式。
- **文件**：套用完整的檢查清單。這裡精確性很重要，所以修正之後，確認繫動詞與詞彙替換沒有弱化技術主張（把「robust error handling」刪成「error handling」沒問題；把「handles all EXIF variants」弱化成「handles EXIF」就不行）。
- **書信往來**：套用完整的檢查清單，同時保留作者的專業語域。移除模式時，不要把一封直接的電子郵件變得更生硬。
- **面向大眾的文案**（網站文案、行銷、App 商店文字、品牌的社群貼文）：完整檢查清單，加上語氣錨點中的禁用詞檢查。這是殘留破綻代價最高的語域。

## 本技能絕不用於

- 從零產生新的文案。它只編修使用者有權編修的既有文字。新文案請使用獨立的撰稿流程。
- 加長或「改善」論點、語氣或說服力。
- 超出標記明顯、確定錯誤範圍的事實查核。這不是研究輪次。
- 質疑作者的意見、主張，或不在上述模式清單中的用字選擇。
- 偵測第三方的文字是否為機器所寫，或給出作者身分的百分比或判決。偵測模式只會點名經授權之草稿中出現的模式。它絕不宣稱作者身分，也不產生信心分數。
