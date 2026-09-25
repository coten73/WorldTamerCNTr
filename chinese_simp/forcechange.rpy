init -997 python:
    import re
    CN_DYNAMIC_NAMES = {
        "Lisa",
        "Rose",
        "Abigail",
        "Amber",
        "Jade",
        "Aqua",
        "Astra",
        "Aurora",
        "Ava",
        "Chloe",
        "Cynthia",
        "RaccoonGirl",
        "Daisy",
        "Diana",
        "Ellie",
        "Kaia",
        "Emily",
        "Emma",
        "Freya",
        "Hannah",
        "Liv",
        "Helen",
        "Luna",
        "Iris",
        "Ivy",
        "Jenny",
        "Julia",
        "Katherine",
        "Kora",
        "Layla",
        "Leah",
        "Lily",
        "Lucy",
        "Megan",
        "Mia",
        "Nadia",
        "Naomi",
        "Nora",
        "Nova",
        "Think",
        "Quila",
        "Jill",
        "Roxie",
        "Sally",
        "Sarah",
        "Katie",
        "Lana",
        "Selene",
        "Sophia",
        "Talia",
        "Tara",
        "Valerie",
        "Zoe",
        "Silas",
        "Sam",
    }
    CN_BRACKET_REPLACE = {}
    for name in CN_DYNAMIC_NAMES:
        if name in CN_REPLACE:
            CN_BRACKET_REPLACE["[" + name.lower() + "]"] = CN_REPLACE[name]

init -998 python:
    import re
    old_text_init = renpy.text.text.Text.__init__
    old_replace_text = config.replace_text
    def cn_replace_text(text):
        if isinstance(text, str):
            if renpy.game.preferences.language == "chinese_simp":
                if text in CN_REPLACE:
                    return CN_REPLACE[text]
        if old_replace_text:
            return old_replace_text(text)
        return text
    config.replace_text = cn_replace_text
    def new_text_init(self, text, *args, **kwargs):
        if isinstance(text, str) and renpy.game.preferences.language == "chinese_simp":
            if "[Luna]" in text:
                text = text.replace("[Luna]", "[luna]")
            elif text.startswith("[") and text.endswith("]"):
                try:
                    final_text = renpy.substitute(text)
                    if final_text in CN_REPLACE:
                        text = CN_REPLACE[final_text]
                except Exception:
                    pass
            elif text.startswith("{=fm}"):
                plain_text = text[5:]
                if plain_text in CN_REPLACE:
                    text = CN_REPLACE[plain_text]
                    kwargs["font"] = "tl/chinese_simp/NotoSerifCJKsc-Bold.otf"
                    kwargs["size"] = 72
                    kwargs["yoffset"] = -23
            elif kwargs.get("style") == "text":
                for old, new in sorted(
                    CN_REPLACE.items(),
                    key=lambda item: len(item[0]),
                    reverse=True
                ):
                    pattern = (
                        r"(?<![A-Za-z0-9_'])"
                        + re.escape(old)
                        + r"(?![A-Za-z0-9_'])"
                    )
                    text = re.sub(pattern, new, text)
            elif kwargs.get("style") == "say_label":
                if text in CN_REPLACE:
                    text = CN_REPLACE[text]
            elif text == "Talk to [luna]" and persistent.voiceName == "Luna":
                text = "与露娜交谈"
        old_text_init(self, text, *args, **kwargs)
    renpy.text.text.Text.__init__ = new_text_init

init -996 python:

    # ======================================================================
    #  插值值翻译 hook
    #  ----------------------------------------------------------------------
    #  问题根源（已在 renpy/substitutions.py 8.5.3 源码确认）:
    #
    #      Text.set_text()
    #        -> renpy.substitutions.substitute(s, scope, substitute)
    #               s = renpy.translation.translate_string(s)      # ① 先翻译整句
    #               s = renpy.substitutions.interpolate(s, scope)  # ② 后插值
    #
    #  所以 "Talk [pregnancyTalk] (talk)" 在 ① 阶段还是原始英文串，
    #  [pregnancyTalk] 直到 ② 才变成 "(Pregnancy)"，
    #  CN_REPLACE["Pregnancy"] / config.replace_text / Text.__init__
    #  都不可能命中。
    #
    #  落点: interpolate() 内部 `value = scope[code]` 之后、`format(value, fmt)`
    #  那一刻。把 scope 里「简单变量名」的 str 值包成 _CNString(str)，
    #  由 _CNString.__format__ 对这一段 piece 做一次 CN_REPLACE 精确匹配，
    #  不碰字面量、不扫描整句。
    #
    #      [pregnancyTalk] -> "(Pregnancy)" -> CN_REPLACE -> "（怀孕）"
    #
    #  顺带解决第二类: Ren'Py 的 interpolate 是单趟的，插值出来的值里面
    #  再有的 [xxx] 没有任何人展开。典型例子
    #  game/tl/chinese_simp/scripts/profiles.rpy:35
    #      new "我应该下午去瑜伽馆拜访她和 [lily]。"
    #  这句存进 katherineSideHint，随后以 [charSideHintDesc] 的形式插进
    #  screen，于是 [lily] 就原样显示成 "[lily]"。所以 __format__ 在
    #  CN_REPLACE 未命中且值里还有 "[" 时，会用同一个 scope 再补一趟
    #  interpolate，把里面的 [lily] 展开成 莉莉。
    #
    #  第三类: 中文翻译里写坏的 [Xxx] 占位符。
    #  翻译 pack 把 "Sophia" 写成了 [Sophia]，但 store 里只有小写变量
    #  sophia，这类 token 会直接 NameError。插值前把「没定义、但小写有
    #  定义」的名字退回小写: [Sophia] -> [sophia] -> 索菲娅。
    #
    #  第四类: 译文里残留的裸英文名（"让 Lisa 租一个房间"）。
    #  只收译文里确实出现的那 15 个名字，译名取自 CN_REPLACE，
    #  且整串必须已经含中文才生效。
    #
    #  三道安全闸门:
    #    1. 只在 language == "chinese_simp" 时生效。
    #    2. 只在 substitute(..., translate=True) 调用链（给人看的文本）里生效。
    #       图片/音频名走 renpy.easy.dynamic_image(..., translate=False)，
    #       那里的 [roseLocation] / [currentPeriod] 不会被翻译，不会丢图；
    #       [Xxx] 大小写修正和裸英文名替换在那边也一律不生效。
    #    3. 只处理单个简单变量名（SIMPLE_NAME）、值类型正好是 str；
    #       CN_REPLACE 是整段精确匹配，不是子串替换。
    # ======================================================================

    try:

        import collections as _cn_collections

        # ==================================================================
        #  中文翻译里写坏的 [Xxx] 占位符
        #  ------------------------------------------------------------------
        #  翻译 pack 里把 "Sophia" 写成了 [Sophia]，但 store 里只有小写
        #  的 sophia（Character）。这类 token 会直接 NameError，
        #  这里在插值前把「没定义、但小写有定义」的名字退回小写。
        #     [Sophia] -> [sophia]   [Astra] -> [astra]   [Lily] -> [lily]
        #  已经定义的大写变量、以及 [charSideHintDesc] / [count] / [url]
        #  这类正常 token 一律不动。
        # ==================================================================
        _cn_token_re = re.compile(r"(?<!\[)\[([A-Za-z_][A-Za-z0-9_]*)\]")

        _CN_TOKEN_FIX = {
            "rigthP": "rightP",
        }

        def _cn_fix_tokens(s, scope):

            if "[" not in s:
                return s

            def repl(m):

                name = m.group(1)

                fixed = _CN_TOKEN_FIX.get(name)

                if fixed is None:
                    low = name.lower()
                    if (name != low) and (name not in scope) and (low in scope):
                        fixed = low

                if fixed is None:
                    return m.group(0)

                return "[" + fixed + "]"

            return _cn_token_re.sub(repl, s)

        # ==================================================================
        #  裸英文名
        #  ------------------------------------------------------------------
        #  翻译里还剩 "让 Lisa 租一个房间" 这种裸英文名。只收译文里确实
        #  残留的这 15 个，译名直接取自 CN_REPLACE（唯一手工维护的词典），
        #  绝不遍历整个 CN_REPLACE，所以日期 / 地点 / UI 词不会被误伤。
        #  额外要求：整串里必须已经有中文，纯英文串原样不动。
        # ==================================================================
        _CN_BARE_NAME_KEYS = [
            "Rose", "Ava", "Lisa", "Layla", "Emily", "Astra", "Emma", "Kora",
            "Roxie", "Aurora", "Quila", "Ivy", "Julia", "Cynthia", "Katherine",
        ]

        _CN_BARE_NAMES = {
            _n: CN_REPLACE[_n] for _n in _CN_BARE_NAME_KEYS if _n in CN_REPLACE
        }

        _cn_bare_re = None

        if _CN_BARE_NAMES:
            _cn_bare_re = re.compile(
                r"(?<![A-Za-z0-9_'])("
                + "|".join(sorted(_CN_BARE_NAMES, key=len, reverse=True))
                + r")(?![A-Za-z0-9_'])"
            )

        _cn_cjk_re = re.compile(u"[\u3400-\u9fff\uf900-\ufaff]")

        def _cn_bare_names(s):

            if (not isinstance(s, str)) or (_cn_bare_re is None):
                return s

            if _cn_cjk_re.search(s) is None:
                return s

            if _cn_bare_re.search(s) is None:
                return s

            return _cn_bare_re.sub(lambda m: _CN_BARE_NAMES[m.group(1)], s)

        # ==================================================================
        #  个别变量的内容修补
        #  ------------------------------------------------------------------
        #  company.rpy:2252  $ datingList = ", ".join(girlsDating[:-1]) + " and " + girlsDating[-1]
        #  拼出来是 "Lisa, Rose and Emily"，里面是英文连接词。
        # ==================================================================
        _CN_VALUE_FIXES = {
            "datingList": ((r",\s*", u"、"), (r"\s+and\s+", u"和")),
        }

        class _CNString(str):
            """
            str 子类，只重写 __format__。

            interpolate() 里那一步是 `rv += format(value, fmt)`，
            format() 会调用 type(value).__format__ —— 这正是包装的入口。

            做两件事:
              1. 整段能在 CN_REPLACE 里精确命中就换成中文。
              2. 命中不了、但值本身还带 [xxx]（典型例子: 中文翻译写成
                 "我应该下午去瑜伽馆拜访她和 [lily]。"），就借着同一个
                 scope 再跑一趟 interpolate，把里面的 [lily] 展开。
                 因为 Ren'Py 的 interpolate 是单趟的 —— 插值出来的值
                 里面再有的 [xxx] 正常情况下永远不会被处理。
            """

            def __new__(cls, value, scope=None):
                rv = str.__new__(cls, value)
                rv._cn_scope = scope
                return rv

            def __format__(self, format_spec):

                piece = CN_REPLACE.get(self)

                if piece is None:

                    piece = str.__format__(self, "")

                    if ("[" in piece) and (piece not in _cn_expanding):

                        key = piece
                        _cn_expanding.add(key)

                        try:
                            piece = renpy.substitutions.interpolate(piece, self._cn_scope)
                        except Exception:
                            piece = str.__format__(self, "")
                        finally:
                            _cn_expanding.discard(key)

                return format(piece, format_spec)

        _cn_name_cache = {}

        def _cn_simple_names(s):

            rv = _cn_name_cache.get(s)
            if rv is not None:
                return rv

            names = set()

            for _lit, expr, _conv, _fmt in renpy.substitutions.parse(s):

                if expr is None:
                    continue

                code = expr.strip()

                if code.endswith("="):
                    code = code[:-1].strip()

                if code and renpy.substitutions.SIMPLE_NAME.match(code):
                    names.add(code)

            rv = frozenset(names)

            if len(_cn_name_cache) > 8192:
                _cn_name_cache.clear()

            _cn_name_cache[s] = rv

            return rv

        _cn_active = [0]

        _cn_expanding = set()

        def _cn_enabled():
            """只有简体中文才启用。"""
            try:
                return renpy.game.preferences.language == "chinese_simp"
            except Exception:
                return False

        _cn_hooked = getattr(renpy.substitutions.interpolate, "_cn_hooked", False)

        if not _cn_hooked:
            _cn_old_interpolate = renpy.substitutions.interpolate
            _cn_old_substitute = renpy.substitutions.substitute

        def _cn_interpolate(s, scope):

            if (not _cn_active[0]) or (scope is None) or (not isinstance(s, str)) or ("[" not in s):
                return _cn_old_interpolate(s, scope)

            s = _cn_fix_tokens(s, scope)

            try:
                subset = {}

                for name in _cn_simple_names(s):
                    try:
                        value = scope[name]
                    except Exception:
                        continue

                    if type(value) is str:

                        fix = _CN_VALUE_FIXES.get(name)
                        if fix is not None:
                            for pat, rep in fix:
                                value = re.sub(pat, rep, value)

                        subset[name] = _CNString(value, scope)

                if subset:
                    scope = _cn_collections.ChainMap(subset, scope)

            except Exception:
                pass

            return _cn_old_interpolate(s, scope)

        def _cn_substitute(s, scope=None, force=False, translate=True):

            if (not translate) or (not _cn_enabled()):
                return _cn_old_substitute(s, scope=scope, force=force, translate=translate)

            _cn_active[0] += 1

            try:
                rv, did = _cn_old_substitute(s, scope=scope, force=force, translate=translate)
            finally:
                _cn_active[0] -= 1

            rv = _cn_bare_names(rv)

            return rv, did

        if not _cn_hooked:

            _cn_interpolate._cn_hooked = True
            _cn_substitute._cn_hooked = True

            renpy.substitutions.interpolate = _cn_interpolate
            renpy.substitutions.substitute = _cn_substitute

        def cn_debug(s):
            _cn_active[0] += 1
            try:
                return _cn_old_substitute(s, force=True)[0]
            finally:
                _cn_active[0] -= 1

    except Exception as e:
        print("[cn_interpolate_hook] 安装失败（游戏继续运行，插值翻译未启用）:", e)

# 源码 scripts/Characters/{astra,aurora,emily,layla,lisa,naomi,rose,sarah}.rpy
# 菜单项原文是 "Talk [pregnancyTalk] (talk)"，现有 tl 条目写成
# "Talk [pregnancyTalk]"（少了 "(talk)"），与当前版本源码不匹配，
# 所以整句翻译一直不生效。
translate chinese_simp strings:
    old "Talk [pregnancyTalk] (talk)"
    new "对话[pregnancyTalk]（对话）"

init -995 python:

    CN_CJK_FONT = "fonts/NotoSansSC-SemiBold.ttf"

    # fm 中文字形的垂直修正比例，原作者在 {=fm} 分支里用的 -23 @ size 72。
    # 觉得还偏就改这一个数（负数=上移）。
    CN_FM_OFFSET = -23.0 / 72.0

    def cn_font_group(latin_font):

        rv = FontGroup()

        rv.add(latin_font, 0x0020, 0x007e)
        rv.add(latin_font, 0x00a0, 0x00ff)
        rv.add(latin_font, 0x2010, 0x205e)
        rv.add(latin_font, 0x20a0, 0x20bf)
        rv.add(CN_CJK_FONT, None, None)

        return rv

    CN_FONT_FM = cn_font_group("fonts/Freshman.ttf")
    CN_FONT_PC = cn_font_group("fonts/PartyConfettiRegular.ttf")
    CN_FONT_COOL_RG = cn_font_group("fonts/coolvetica rg.otf")
    CN_FONT_ITEM_POPUP = cn_font_group("fonts/PartyConfettiRegular.ttf")
    CN_FONT_MENU_VERSION = cn_font_group("fonts/coolvetica rg.otf")
    CN_FONT_SUPPORTERS = cn_font_group("fonts/Roboto-BoldCondensed.ttf")


init -994 python:

    # ==================================================================
    #  fm 风格下的中文字形会往下沉
    #  ------------------------------------------------------------------
    #  style fm 原本是 Freshman.ttf，行高和基线是按它调的。换成中文字形
    #  之后 baseline 变了，文字整体下沉。原作者在 {=fm} 分支里已经用
    #  yoffset = -23（size 72）修正过，这里对「实际会显示中文的 fm 文本」
    #  按同一个比例补上，size 变化时按比例缩放。
    #
    #  注意：fm 文本在 Text.__init__ 时还是 "{=fm}Luna{/=}" 这种纯英文，
    #  中文是后面 config.replace_text 按 token 命中 CN_REPLACE 才出现的，
    #  translate_string 查不到。所以这里要去掉标签后自己探一遍。
    # ==================================================================

    _cn_tag_re = re.compile(r"\{[^}]*\}")

    if not getattr(renpy.text.text.Text.__init__, "_cn_text_hooked", False):

        _cn_old_text_init = renpy.text.text.Text.__init__

        def _cn_fm_shows_cjk(text):

            plain = _cn_tag_re.sub("", text).strip()

            if not plain:
                return False

            cands = [plain]

            hit = CN_REPLACE.get(plain)
            if hit is not None:
                cands.append(hit)

            try:
                cands.append(renpy.translation.translate_string(plain))
            except Exception:
                pass

            try:
                cands.append(renpy.substitutions.substitute(text, force=True)[0])
            except Exception:
                pass

            for i in cands:
                if isinstance(i, str) and _cn_cjk_re.search(i) is not None:
                    return True

            return False

        def _cn_text_init(self, text, *args, **kwargs):

            if isinstance(text, str) and ("yoffset" not in kwargs) and _cn_enabled():

                _fm = text.startswith("{=fm}") or (kwargs.get("style") == "fm")

                if _fm and _cn_fm_shows_cjk(text):
                    _size = kwargs.get("size")
                    if not _size:
                        try:
                            _size = style.fm.size
                        except Exception:
                            _size = 72
                    kwargs["yoffset"] = int(round(CN_FM_OFFSET * _size))

            _cn_old_text_init(self, text, *args, **kwargs)

        _cn_text_init._cn_text_hooked = True
        renpy.text.text.Text.__init__ = _cn_text_init

    # ==================================================================
    #  [luna] 一直显示 "Luna"
    #  ------------------------------------------------------------------
    #  define luna = Character("[persistent.voiceName]")
    #  Character.__str__ 会对名字跑一遍 substitute，但 substitute 是
    #  「先 translate_string、后 interpolate」—— persistent.voiceName
    #  展开出来的 "Luna" 是在插值阶段才出现的，所以永远没人翻译它。
    #  这里对角色显示名补一次查表（CN_REPLACE -> 翻译表），顺带解决所有
    #  「动态角色名」的同类问题。
    #
    #  注意类名是 ADVCharacter：renpy.character.Character 是个工厂函数，
    #  往它身上挂 __str__ 是没用的。
    #  renpy.input 的默认值走的是 [persistent.voiceName] 插值，不经过
    #  Character，所以改名输入框里仍然是 "Luna"，不会被写进存档。
    # ==================================================================

    if not getattr(renpy.character.ADVCharacter.__str__, "_cn_hooked", False):

        _cn_old_char_str = renpy.character.ADVCharacter.__str__

        def _cn_char_str(self):

            rv = _cn_old_char_str(self)

            if _cn_enabled() and isinstance(rv, str):
                hit = CN_REPLACE.get(rv)
                if hit is None:
                    hit = renpy.translation.translate_string(rv)
                if hit != rv:
                    return hit

            return rv

        _cn_char_str._cn_hooked = True
        renpy.character.ADVCharacter.__str__ = _cn_char_str



translate chinese_simp style fm:
    font CN_FONT_FM

translate chinese_simp style pc:
    font CN_FONT_PC

translate chinese_simp style cool_rg:
    font CN_FONT_COOL_RG

translate chinese_simp style item_popup_style:
    font CN_FONT_ITEM_POPUP

translate chinese_simp style menu_version:
    font CN_FONT_MENU_VERSION

translate chinese_simp style text_for_supporters:
    font CN_FONT_SUPPORTERS
