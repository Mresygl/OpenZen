# Zen 抄袭 Naven 的源代码证据

本文档基于公开可获取的两个仓库进行**逐行 / 逐字段 / 逐字符串**对比：

- **参考实现（被抄袭方）**：[`Margele/Naven-Modern`](https://github.com/Margele/Naven-Modern)（即 Naven 客户端的简单移植版本）
- **待审项目（疑似抄袭方）**：本仓 OpenZen（Zen 客户端反混淆产物）

> Naven 仓库的包名混淆 `com.heypixel.heypixel.VcX6svVqmeT8.*` 来自 Naven 原作者本人 push 上 GitHub 的状态，不是本文档的混淆操作。Zen 这边的对应文件全部位于 `src/main/java/shit/zen/`。

---

## TL;DR

- **Zen 的"功能模块"几乎全部能在 Naven 中找到一对一对应**：要么直接同名搬运，要么把 Naven 的 `@ModuleInfo(name=...)` 内部名直接拿来当类名（最典型的是 `InventoryManager` —— Naven 的类叫 `InventoryCleaner`，但 `@ModuleInfo(name="InventoryManager")`，Zen 直接以这个内部名命名）。
- **框架层（事件 / 模块 / 设置 / 命令 / 工具）也全套搬运**：`EventBus` 是 Naven `EventManager` 的逐字段重命名；`EventPriority` 沿用 DarkMagician6 EventAPI 的特征数值；`@EventTarget value() default 2` 完全一致；`bind/toggle/config/language` 四条命令的提示串（`"Bound X to Y."`、`"Invalid module."`、`"Usage: .bind <module> [key]"`）一字不差；`ChunkUtil.getLoadedChunks` 连异常文案 `"Stream limit didn't work."` 都照搬。
- **多处遗留"反混淆指纹"**：`RotationUtil` 里那个工具类完全用不到的 `import org.antlr.v4.runtime.misc.OrderedHashSet`；`Stuck` 的魔法数 `+ 1337`；`Projectiles` 模块 RGB `(173, 12, 255)` / `(255, 238, 154)`；`InventoryManager` 的中文字面量 `"点击使用"`；都是 Naven 那边独有的特征。
- **改动方向集中在三件事**：（a）拆模块（把 Naven 的 `HUD` 拆成 `Watermark` + 一堆 `shit.zen.hud.*`）；（b）扩写（`Disabler` 在 Naven 的 yaw-only 一段外面包了一整套 Grim/ACA/Themis 子模块）；（c）改名（`AttackCrystal → CrystalAura`、`Aura → KillAura`、`Glow → ESP`、`NoJumpDelay → NoDelay`、`InventoryCleaner → InventoryManager`），通常**只换类名不换 Setting 文案**，所以 Setting 字符串成为最稳定的抄袭指纹。

下表是模块级的总览：

| 类别 | Naven 模块 | Zen 对应 | 抄袭程度 |
|------|-----------|---------|---------|
| Combat | `AntiBots` | `combat/AntiBots` | **逐行** |
| Combat | `Aura` (`@ModuleInfo name="KillAura"`) | `combat/KillAura` | **逐行**（最严重） |
| Combat | `AttackCrystal` (`@ModuleInfo name="CrystalAura"`) | `combat/CrystalAura` | **逐行** |
| Combat | `AntiFireball` | `combat/AntiFireball` | **逐行** |
| Combat | `AimAssist` | `misc/AimAssist` | 同名 + 部分重写 |
| Combat | `AutoClicker` | `misc/AutoClicker` | 同名 + 显著扩写 |
| Combat | `Velocity` | `combat/AntiKB` | 仅功能相近，不构成抄袭 |
| Move | `Scaffold` | `movement/Scaffold` | **逐行** + 扩展 |
| Move | `FastWeb` | `movement/FastWeb` | **逐行** |
| Move | `Sprint` | `movement/Sprint` | **逐行** |
| Move | `Stuck` | `player/Stuck` | **逐行** + 扩展 |
| Move | `AutoMLG` | `player/AutoMLG` | 重写 + 触发器抄袭 |
| Move | `SafeWalk` | `misc/SafeWalk` | **逐行**（仅改 Category） |
| Move | `Blink` | `movement/FireballBlink` | 骨架抄袭 + 场景重写 |
| Move | `NoJumpDelay` | `movement/NoDelay` | 改名（Setting label 露馅） |
| Misc | `Disabler` | `exploit/Disabler` | 核心段照搬 + 包装扩展 |
| Misc | `FastPlace` | `exploit/FastPlace` | hook 入口一致，算法换皮 |
| Misc | `AutoTools` | `world/AutoTools` | **逐行翻译** |
| Misc | `Teams` | `world/Teams` | **逐行**（加一个 Mode） |
| Misc | `ChestStealer` | `player/ChestStealer` | 核心判定段照搬 |
| Misc | `InventoryCleaner` (`@ModuleInfo name="InventoryManager"`) | `player/InventoryManager` | **逐行**（含中文字面量） |
| Render | `Glow` | `render/ESP` | 改名 + 扩展 |
| Render | `ChestESP` | `render/ChestESP` | **逐行** |
| Render | `Compass` | `render/Compass` | **逐行** |
| Render | `FullBright` | `render/FullBright` | **逐行**（仅放大范围） |
| Render | `ItemTags` | `render/ItemTags` | 同名空壳 |
| Render | `NameProtect` | `render/NameProtect` | 同算法 + 重写事件路径 |
| Render | `NameTags` | `render/NameTags` | 门面策略类（Scale=0.3/0.01 露馅） |
| Render | `NoHurtCam` | `render/NoHurtCam` | 同名空壳 |
| Render | `Projectile` | `render/Projectiles` | **逐行**（颜色/重力/算法常量全照搬） |
| Render | `HUD` | `render/Watermark` + `shit.zen.hud.*` | 拆模块 + 字段名 |
| 框架 | `EventManager` / `EventTarget` / `Priority` | `EventBus` / `EventTarget` / `EventPriority` | **逐字段** |
| 框架 | `Module` / `ModuleManager` / `Category` | 同名 | **逐行**（setEnabled、toggle 完全一致） |
| 框架 | `Value` / `ValueBuilder` / `*Value` | `Setting` / `*Setting` | **同结构**改名 |
| 框架 | `Command*` + `CommandManager` | `Command*` + `CommandManager` | **逐字符串**（命令名、提示串一致） |
| 框架 | `RotationUtils` / `ChunkUtils` / `BlockUtils` / ... | `RotationUtil` / `ChunkUtil` / `BlockUtil` / ... | **逐行** + 残留特征 import |

---

## 一、Combat 模块

### Zen `combat/AntiBots.java` vs Naven `combat/AntiBots.java`

**对应关系**：直接同名搬运。

**关键证据**：

- 五个静态 map 一一对应：`uuidDisplayNames ↔ suspectNames`、`entityIdDisplayNames ↔ confirmedBotNames`、`uuids ↔ suspectJoinTimes`、`ids ↔ confirmedBotIds`、`respawnTime ↔ playerAddTimes`，全部用 `ConcurrentHashMap` / `HashSet`。
- Setting `"Respawn Time"`：默认 2500、范围 0–10000、步长 100，完全一致。
- 方法 `isBedWarsBot(Entity)` / `isBot(Entity)` 签名和返回路径完全相同。
- **字符串字面量原样保留**：`"Fake Staff Detected! ("`、`"Bot Detected! ("`、`"Bot Removed! ("` 三条全部相同。
- 500 ms 怀疑→确认管线、`ClientboundPlayerInfoUpdatePacket / ClientboundAddPlayerPacket / ClientboundRemoveEntitiesPacket` 三段式处理同构。

### Zen `combat/KillAura.java` vs Naven `combat/Aura.java`

**对应关系**：Naven 类名 `Aura`（`@ModuleInfo(name="KillAura")`）→ Zen 直接以 `KillAura` 命名。**这是抄袭最严重的模块。**

**关键证据**：

- **12 个 BooleanSetting + 9 个 NumberSetting 与 Naven 一一对应**，名字/默认值/范围全套一致：`Attack Player / Attack Invisible / Attack Animals / Attack Mobs / Multi Attack / Prefer Baby / Target HUD / Target ESP / Attack Range(=Aim Range) / APS / Switch Size / FOV / Hurt Time`，默认 `range=5/1–6, aps=10/1–20, switchSize=1/1–5, fov=360/10–360, hurtTime=10/0–10`。
- `switchSize` 的可见性 `() -> !infSwitch.getValue()` 等价 Naven `() -> !infSwitch.getCurrentValue()`。
- `isValidTarget` 的实体类型检查链：`ArmorStand / Invisible / Player+bbWidth<0.5 || isSleeping / (Mob|Slime|Bat|AbstractGolem) / (Animal|Squid) / Villager / isSpectator`——import `Bat, AbstractGolem, Squid, Slime, Villager, ArmorStand` 完全一致。
- 主循环：`isSwitch = switchSize > 1` → `updateTargets()` → `aimingTarget = shouldPreAim/getTarget()` → 记录 `prev/lastRotationData` → `attacks >= switchAttackTimes || distance > 3` 时 round-robin `++index` → `attacks += aps/20f`。
- `getTargets()` 结尾：`possibleTargets.sort(Comparator.comparing(o -> o instanceof EndCrystal ? 0 : 1))`、`subList(0, Math.min(size, switchSize))` 限长、`preferBaby` 的 `removeIf(!isBaby)`，三处写法一对一。
- TargetESP：`200/255F, 0, 0, 60/255F` red / `0, 200/255F, 0, 60/255F` green、`AABB box = entity.getBoundingBox().move(-motionX,-motionY,-motionZ).move(partialTick*motionX,...)`、`RenderSystem.setShader(GameRenderer::getPositionShader)`、`GL_LINE_SMOOTH` 开关顺序完全照搬。

### Zen `combat/CrystalAura.java` vs Naven `combat/AttackCrystal.java`

**对应关系**：Naven 类名 `AttackCrystal`（`@ModuleInfo(name="CrystalAura")`）→ Zen 直接以 `CrystalAura` 命名。

**关键证据**：

- Setting `"Attack on Packet (Danger)"` 字符串、`boolean` 类型、`false` 默认完全一致。
- `onPacket` 7 步序列：收 `ClientboundAddEntityPacket` → `EntityType.END_CRYSTAL` → `new EndCrystal(mc.level, packet.getX/Y/Z())` → `setId(packet.getId())` → 距离阈值 `≤ 4` → `ServerboundMovePlayerPacket.PosRot` + `ServerboundUseItemPacket(MAIN_HAND)` → 暂存→改 rotation→`createAttackPacket(target, false)`→swing→还原。一一对应。
- `onTick` 中 `Optional<Entity> any = StreamSupport.stream(... entitiesForRendering ...).filter(entity instanceof EndCrystal).findAny();` 配合 `≤ 3` 阈值。
- 静态字段 `Entity entity / crystalTarget` 与 `rotations / aimRotation` 双字段同构。

### Zen `combat/AntiFireball.java` vs Naven `misc/AntiFireball.java`

**对应关系**：同名搬运（仅改 Category）。

**关键证据**：

- 流式查找一模一样：`StreamSupport.stream(mc.level.entitiesForRendering().spliterator(), …).filter(entity instanceof Fireball && mc.player.distanceTo(entity) < 6).map(...).findFirst()`，距离阈值 `6` 同。
- 早退 `if (!optional.isPresent()) return;`。
- 两行攻击代码顺序和变量名完全一致：`mc.gameMode.attack(mc.player, fireball); mc.player.swing(InteractionHand.MAIN_HAND);`。

### Zen `misc/AimAssist.java` vs Naven `combat/AimAssist.java`

**对应关系**：同名搬运 + 后续大改写。

**关键证据**：类名同；`getAngleDifference(double, double)` 静态助手同名同实现（`Mth.wrapDegrees(a-b)`）；`fov` / `range` 字段语义相同（Setting label `"Fov"` / `"FoV"` 仅大小写差）。

**改动**：算法已大幅重写为 smooth/adaptive 偏移模型，事件接入 `KillAura.isValidTarget(...)`，逐行抄袭已不显著。

### Zen `misc/AutoClicker.java` vs Naven `combat/AutoClicker.java`

**对应关系**：同名搬运 + 显著扩写。

**关键证据**：核心攻击路径相同 —— `mc.options.keyAttack.isDown()` + `mc.hitResult.getType() != BLOCK` + `setMissTime(0)`（Naven 通过 `MinecraftAccessor` mixin，Zen 通过 `ReflectionUtil`） + `KeyMapping.click(mc.options.keyAttack.getKey())`。

**改动**：Zen 加 Left/Right/Both、Method/Key/Mouse、Break Block、CPS Mode 等扩展。

### Zen `combat/AntiKB.java` vs Naven `combat/Velocity.java`

**判定**：功能相近但实现路径完全不同（Zen 是 mode-dispatcher，Naven 是 packet-cancel），**不构成抄袭证据**。

---

## 二、Movement / Player 模块

### Zen `movement/Scaffold.java` vs Naven `move/Scaffold.java`

**对应关系**：同名搬运，框架翻新但核心算法逐句保留。

**关键证据**：

- `ModeSetting("Mode", "Normal", "Telly Bridge", ..., "Keep Y")` 与 Naven `mode.setModes("Normal","Telly Bridge","Keep Y")` 一一对应。
- `renderItemSpoof` 字段名、默认 `true` 一致；`advancedBlockSearch` 字段名原样保留。
- `eagle` / `snap` 的可见性 lambda `() -> mode.is("Normal")` 与 Naven `setVisibility(() -> mode.isCurrentMode("Normal"))` 是相同代码翻译。
- `getPlayerYawRotation` 中随机抖动 `RandomUtils.nextFloat(0.0f, 0.5f) - 0.25f`、yaw `-180.0F`、pitch `82F / 75.5F` 这些 magic 数原样保留。
- **`isOnBlockEdge(float)` 函数体逐字符相同**：`!mc.level.getCollisions(mc.player, mc.player.getBoundingBox().move(0.0,-0.5,0.0).inflate(-x,0.0,-x)).iterator().hasNext()`。

### Zen `movement/FastWeb.java` vs Naven `move/FastWeb.java`

**关键证据**：

- 字段 `playerInWebTick / ticksInWeb`（Naven）→ `lastWebTick / webCount`（Zen）只改名不改语义。
- `onMotion` 中 `playerInWebTick < mc.player.tickCount → ticksInWeb = 0` 的 reset 逻辑完全照搬。
- 阈值 `> 5` 与魔法向量 `new Vec3(0.88, 1.88, 0.88)` **逐字节相同**。
- 无 Setting，行为路径一致。

### Zen `movement/Sprint.java` vs Naven `move/Sprint.java`

**关键证据**：类签名一致，主体只有 `mc.options.toggleSprint().set(false)` + `keySprint` 强按下，PRE 阶段执行。

### Zen `player/Stuck.java` vs Naven `move/Stuck.java`

**关键证据**：

- 字段一一对应（仅重命名）：`stage / packet / lastYaw / lastPitch / tryDisable / Queue<ServerboundPongPacket> packets` → `stuckState / capturedPacket / savedYaw / savedPitch / pendingDisable / pongQueue`。
- `setEnabled` 的 `stage==3 → disable`、否则 `tryDisable=true` 三段分支完全保留。
- **神奇位移常数 `mc.player.getX() + 1337` / `getZ() + 1337` 一字不差。**
- `onPacket` 的 `instanceof` 链顺序与分支体一致：`ServerboundMovePlayerPacket → cancel`、`ServerboundPongPacket → offer + cancel`、`ServerboundUseItemPacket || ServerboundPlayerActionPacket → capture + stage=1 + cancel`、`ClientboundPlayerPositionPacket → drain pong + stage=3 + disable`。

### Zen `player/AutoMLG.java` vs Naven `move/AutoMLG.java`

**关键证据**：

- Setting `triggerDistanceSetting = NumberSetting("Fall distance", 3.0f, 1.0f, 10.0f, 0.1f)` 与 Naven `distance = ValueBuilder("Fall Distance").setDefaultFloatValue(3).setFloatStep(0.1f)...` 默认/步进相同。
- `Items.WATER_BUCKET` 在槽 0..9 的扫描写法、`originalSlot = inventory.selected` 切换+还原模式照搬。
- pitch 强制朝下（90°）、useItem MAIN_HAND + swing 流程一致。

**Zen 自加**：Predict Ticks / Solid check / 一个拼写错误 `Recorvey`（typo，反而成为抄袭佐证）。

### Zen `misc/SafeWalk.java` vs Naven `move/SafeWalk.java`

**关键证据**：

- `isOnBlockEdge(float)` 函数体**逐字符相同**（含 `0.3F` 常量、参数 `inset` 是 `sensitivity` 的最小程度改名）。
- `onMotion` 主体一句 `mc.options.keyShift.setDown(mc.player.onGround() && isOnBlockEdge(0.3F))`。
- `onDisable` 复用 `InputConstants.isKeyDown(...) + mc.options.keyShift.setDown` 模式。

**改动**：仅改 Category（MOVEMENT → MISC）。

### Zen `movement/FireballBlink.java` vs Naven `move/Blink.java`

**对应关系**：Naven 通用 `Blink` 被改名为 `FireballBlink` 并特化场景。

**关键证据**：`LinkedBlockingQueue<Packet<?>> + ConcurrentLinkedQueue` 的"扣留发包再 flush"骨架、`flushPackets()` 在 disable 时清队列、监听 `ClientboundSetEntityMotionPacket` 玩家 ID 后入队，与 Naven 的 packet 暂存模型同构。

### Zen `movement/NoDelay.java` vs Naven `move/NoJumpDelay.java`

**关键证据**：

- Setting label `new BooleanSetting("No Jump Delay", true)` **直接抄 Naven 的 `@ModuleInfo(name="NoJumpDelay")`**。
- 字段名 `fastDig` 与开关 label 不符 —— 提示是从其它项目搬来后未对齐。
- 类本身没有事件回调，实际效果由 mixin 完成（同 Naven 的 `LivingEntityAccessor.setNoJumpDelay(0)` 思路）。

---

## 三、Misc / Exploit / Player 模块

### Zen `exploit/Disabler.java` vs Naven `misc/Disabler.java`

**对应关系**：Naven Disabler 的 `duplicateRotPlaceDisabler` 一整段被 Zen 当作 `grimDuplicateRotPlace` 子选项原样搬来，外面包了一整套扩展。

**关键证据**：

- 字段命名完全照搬：`rotated`、`lastPlacedDeltaYaw → lastPlacedYawDiff`、`lastPlacedDeltaPitch → lastPlacedPitchDiff`。
- 算法控制流逐句对应：`hasRotation()` → 算 `deltaYaw = abs(yaw - last)` → `rotated = true` → `ServerboundUseItemOnPacket` 分支 `lastPlacedDeltaYaw = deltaYaw; rotated = false`。
- **魔法常数照抄**：阈值 `deltaYaw > 2`、`xDiff < 0.0001` 完全一致。
- `Logging` BooleanSetting + `log(...)` 函数同名同语义。

**改动**：把生成新 packet 改成 `ReflectionUtil.setYRot/setXRot` 改原 packet；外加 Grim/ACA/Themis 一堆扩展子模块。原始 yaw-only 核心是 Naven 的。

### Zen `exploit/FastPlace.java` vs Naven `misc/FastPlace.java`

**判定**：算法换皮（Zen Delay 计时器，Naven CPS 累加器）但**底层 hook 点 `setRightClickDelay(0)` 完全一致**（Naven 通过 MinecraftAccessor mixin，Zen 通过 ReflectionUtil）。`BlockItem` 判定路径相同。最弱的证据。

### Zen `world/AutoTools.java` vs Naven `misc/AutoTools.java`

**对应关系**：几乎逐行翻译。

**关键证据**：

- 三个 Setting `"Check Sword"=true`、`"Switch Back"=true`、`"Silent"=true` 字符串和默认值全照搬；`Silent` 绑在 `switchBack` 可见性下也保留。
- 状态字段 `originSlot = -1` → `previousSlot = -1` 仅改名。
- `getBestTool` 算法逐行复制：`int slot=0; float dmg=1; for i in 0..9` → `isGodItem/isWeaponItem` 跳过 → `SwordItem instanceof && !(WebBlock)` 例外 → `destroySpeed > 1` 时加 `efficiencyLevel * efficiencyLevel + 1` 附魔加成 → `dmg > 1 ? slot : -1` 返回。
- `onMotion` PRE/POST 切换逻辑同形，`onUpdateHeldItem` 在 MAIN_HAND && originSlot != -1 时用 `e.setItem(...)` 同一句话。

### Zen `world/Teams.java` vs Naven `misc/Teams.java`

**关键证据**：

- `isSameTeam(Entity)` 签名、返回路径、`instanceof Player` 后调 `getTeam(player) / getTeam(mc.player)` 用 `Objects.equals` 比较——完全一致。
- `getTeam(Entity)` 函数 `mc.getConnection().getPlayerInfo(entity.getUUID()) → null 检查 → playerInfo.getTeam().getName()` 逐行对应。

**改动**：加一个 `ModeSetting("Mode", "Color", "Scoreboard")`，`Scoreboard` 分支就是 Naven 原版。

### Zen `player/ChestStealer.java` vs Naven `misc/ChestStealer.java`

**关键证据**：

- 容器标题判定一模一样：`Component.translatable("container.chest")`、`"container.chestDouble"`、`"container.enderchest"`，再 `|| title.equals("Chest")`。
- `Ender Chest` BooleanSetting 默认 `false` 同名搬过来。
- `isWorthStealing` 是 Naven `isItemUseful` 分支级翻译：`ArmorItem → protection vs BestArmorScore`、`SwordItem → damage`、`PickaxeItem / AxeItem / ShovelItem → ToolScore`、`CrossbowItem → score`、`BowItem + PunchBow / PowerBow` 两个变体、`COMPASS → !hasItem`、`WATER_BUCKET/LAVA_BUCKET >= count`、`BlockItem + isPlaceable + maxBlock`、`ARROW + maxArrow`、`FISHING_ROD >= 1`、`SNOWBALL/EGG + maxProjectile`、`ItemNameBlockItem → false` → `isCommonItemUseful`，**分支顺序与返回逻辑完全一致**。
- 容器步进算法同形：`for (slot=0; slot<chestMenu.getRowCount()*9; slot++)` + `handleInventoryMouseClick(containerId, slot, 0, ClickType.QUICK_MOVE, mc.player)`。
- 跨模块耦合：Zen `ChestStealer.isRateLimited()` 给 `InventoryManager` 用，等价 Naven `ChestStealer.isWorking()`（同样 3 tick timer）。

### Zen `player/InventoryManager.java` vs Naven `misc/InventoryCleaner.java`

**对应关系**：Naven 文件叫 `InventoryCleaner` 但 `@ModuleInfo(name="InventoryManager")`，**Zen 直接用这个内部名作为类名**。

**关键证据**：

- Setting 名几乎一比一：`"Offhand Items"`（含 `Golden Apple / Projectile / Fishing Rod / None / Block` 五选）、`"Auto Armor"`、`"Inventory Only"`、`"Throw Items"`、`"Bow Priority"`（含 `Crossbow / Power Bow / Punch Bow`）、`"Max Eggs & Snowballs Size"`、`"Max Block Size"`、`"Sword Slot" / "Axe Slot" / "Pickaxe Slot" / "Bow Slot" / "Water Bucket Slot" / "Ender Pearl Slot" / "Golden Apple Slot" / "Eggs & Snowballs Slot"`——名称、含义、Slot 1..9 范围全套照抄。
- 默认值匹配：`Max Block Size 256, step 64, 64..512`、`Max Eggs & Snowballs 64, 16..256, step 16`、`Max Arrow 256`。
- 静态 getter API 抄得一字不差：`getMaxBlockSize()`、`getMaxProjectileSize()`、`getMaxArrows()`、`getWaterBucketCount()`、`getLavaBucketCount()` 等。
- **中文字符串字面量原样保留**：Zen `itemStack.getDisplayName().getString().contains("点击使用")` 与 Naven 完全相同。这是最硬的抄袭证据之一。
- 反 GuiMove + ContainerClose 逻辑照搬：`onPacket` 中检测 `ServerboundMovePlayerPacket + isMoving → send ContainerClose`，对 `UseItemOnPacket / UseItemPacket / InteractPacket / PlayerActionPacket` 触发 close，分支顺序完全一致。
- `validateSlotConfig` / `checkConfig` 用 `Pair<Boolean, NumberSetting>` 列表 + `HashSet<Integer> usedSlots` 检测槽位冲突，连 `Pair.of` 这种 commons-lang3 的导入选型都一样。

---

## 四、Render 模块

### Zen `render/ESP.java` vs Naven `render/Glow.java`

**对应关系**：Naven `Glow` 改名为 `ESP` 并扩充为 2D 边框 + 血条。Glow 模式下保留原过滤逻辑。

**关键证据**：

- `ModeSetting("Mode", "Glow", "Outlined 2D")` —— "Glow" 模式即对应 Naven 整个 Glow 模块。
- `isGlowing(Entity)` 分支顺序 `Player → Animal → Mob → ItemEntity → Arrow` 与 Naven `shouldGlow` 的 `Player → ItemEntity → Mob → Animal → Arrow` 高度一致，仅重排。
- 字段 `playersSetting / mobsSetting / animalsSetting / itemsSetting / arrowsSetting` 对应 Naven `players / mobs / animals / items / arrows`，名字 + 类型 + 默认值（Players=true，其余 false）一一对应。

### Zen `render/ChestESP.java` vs Naven `render/ChestESP.java`

**关键证据**：

- 静态字段 `chestColor / openedChestColor` 与初始值 `{0,1,0}` / `{1,0,0}` 完全一致。
- `renderBoundingBoxes` 字段名 + `CopyOnWriteArrayList` 类型完全一致；`openedChestPositions` 仅是 Naven `openedChests` 加后缀。
- `onPacket` 中 `ClientboundBlockEventPacket` 的 `block == CHEST || block == TRAPPED_CHEST && B0 == 1 && B1 == 1` 判定与 Naven 同条件同顺序。
- `getChestAabb` / `getChestBox` 内部逻辑一一对应：`hasProperty(ChestBlock.TYPE)` 返回 null、`ChestType.LEFT` 跳过、`SINGLE` 之外用 `getConnectedDirection + min/max`。
- 着色 `RenderSystem.setShaderColor(fArray[0], fArray[1], fArray[2], 0.25f)` 的 alpha = 0.25 与 Naven `0.25F` 相同。

### Zen `render/Compass.java` vs Naven `render/Compass.java`

**关键证据**：

- 两个 BooleanSetting `"Compass Only"`（默认 true）、`"No Player Only"`（默认 true）名字、默认值完全一致。
- 字段 `spawnPosition / renderYaw / renderX / renderZ` 命名完全一致。
- `getSpawnPosition` 使用 `dimensionType().natural() ? getSharedSpawnPos() : null` 逻辑相同。
- **角度公式字面一致**：`Math.toDegrees(Math.atan2(spawn.z - renderZ, spawn.x - renderX)) - 90 - renderYaw`。
- 提前 return 顺序 `compassOnly → hasPlayer/noPlayerOnly → spawnPosition == null` 完全一致。

### Zen `render/FullBright.java` vs Naven `render/FullBright.java`

**关键证据**：唯一 Setting `"Brightness"` 名字、类型、最小值 0 与 Naven 一致；min/max/step 语义相同（仅把 0–1 缩放到 0–100）。

### Zen `render/NameTags.java` vs Naven `render/NameTags.java`

**关键证据**：模块同名、`Category.RENDER`、事件分发 `onRender / onRender2D / onPacket` 多事件订阅模式一致；`NumberSetting("Scale", 0.3, 0.1, 1.0, 0.01)` 的 **默认 0.3、step 0.01 与 Naven 完全相同**，只把 max 从 0.5 放宽到 1.0。共 6 个 Setting 数量与 Naven 同。

**改动**：把真正实现外包给 `NameTagStyle` 策略类（"Opal" / "Simple"），多数 Setting 名换成新含义掩饰。`Scale` 设置的默认值/step 露馅。

### Zen `render/Projectiles.java` vs Naven `render/Projectile.java`

**关键证据**：

- 5 个 BooleanSetting **完全同名同默认**：`"Show Arrows"=true / "Show Pearls"=true / "Show Potions"=false / "Show Eggs"=false / "Show Snowballs"=false`。
- 颜色字段一一对应且 **RGB 字面量完全相同**：`ThrownEnderpearl → new Color(173, 12, 255)`、`ThrownEgg → new Color(255, 238, 154)`、`Snowball → new Color(255, 255, 255)`。
- `getProjectileGravity` 五个字面常量完全相同：`Bow/Crossbow → 0.05, Potion → 0.4, FishingRod → 0.15, Trident → 0.015, default → 0.03`。
- `isThrowable` 类型集合 9 个 Item 类型相同顺序。
- `simulateTrajectory` 与 Naven `getPath` 同算法：`1000` 步迭代、空气阻力 `0.99`、起点 `getEyeHeight - 0.1`、`bowPower = (p*p + p*2)/3 * 3`。
- `getProjectileInfos` 中 `showArrows → arrowsColor / showPotions → potionsColor / showPearls → enderPearlColor / showEggs → eggColor / showSnowballs → snowballColor` 顺序完全一致。
- 类名 `BasicProjectileData / EntityArrowData / EntityPotionData → ClassEspColor / ArrowEspColor / PotionEspColor` 是包装了一层的重命名。

### Zen `render/Watermark.java` vs Naven `render/HUD.java`

**对应关系**：Zen 把 Naven 的 `HUD` 模块拆分——`Watermark` 只保留水印部分（`Style: Neverlose / DynamicIsland`），ArrayList / Notification 部分迁去 `shit.zen.hud.*`。模块名 `"Watermark"` 直接源自 Naven 的设置名 `"Water Mark"`。

### 其他同名 / 空壳

- `NameProtect`：同算法（`StringUtils.replace`）+ 重写事件路径，加 `Random` 模式。
- `NoHurtCam`：两边都是空壳（实际功能在 mixin 中由模块名查询触发）。
- `ItemTags`：Zen 端是空壳（13 行）。

---

## 五、框架级抄袭（事件 / 模块 / 设置 / 命令 / 工具 / UI）

### 5.1 事件系统

**对应关系**：Zen `EventBus` = Naven `EventManager`（功能 1:1，DarkMagician6 EventAPI 的同源派生）。

**关键证据**：

- 两个类都用 `Map<Class<? extends Event/EventMarker>, List<...>>` 作为唯一存储，注册时 `computeIfAbsent` + `CopyOnWriteArrayList`，注册完调用 `sortListValue / sortByPriority`；Zen 把内部 `MethodData` 改成 record `ListenerEntry`，字段顺序 `source/target/priority` 完全一致。
- 排序逻辑逐行同形：外层遍历 `PRIORITIES`，内层把 `priority() == priority` 的项追加到新 `CopyOnWriteArrayList`，再 `put` 覆盖原 entry——这是 DarkMagician6 EventAPI 的特有写法。
- **优先级数值/数组顺序完全一致**：`HIGHEST=0, HIGH=1, NORMAL/MEDIUM=2, LOW=3, LOWEST=4` + `PRIORITIES = {HIGHEST, HIGH, NORMAL, LOW, LOWEST}`。Zen 仅把 `MEDIUM` 改名 `NORMAL`，类名 `Priority` 改成 `EventPriority`。
- `@EventTarget` 注解：同样 `@Documented @Target(METHOD) @Retention(RUNTIME)`，**方法签名 `byte value() default 2` 完全相同**。
- `call(...)` 分发：先取 `dataList`，判空，再 `instanceof` 取消类（Naven `EventStoppable.isStopped()`、Zen `AbstractCancellable.isCancelled()`），循环里 `break` 提前退出——分支结构、变量命名节奏完全一致。

### 5.2 Module 框架

**关键证据**：

- `Module.setEnabled(boolean)` 实现完全同构：`if (enabled)` 分支 → `this.enabled = true` → `eventManager.register(this)` → `onEnable()`；`else` 分支 → `this.enabled = false` → `eventManager.unregister(this)` → `onDisable()`。`toggle()` 都写成 `setEnabled(!enabled)`。
- 字段 `name / category / key(keyCode) / enabled` 全部存在，都用 Lombok `@Getter`。
- `ModuleManager.onKey(KeyEvent)`：`@EventTarget` 遍历 `modules`，`if (module.getKey() == e.getKey()/getKeyCode()) module.toggle()`，逻辑完全一致。
- 异常 `ModuleNotFoundException` ↔ `NoSuchModuleException` 是直译。
- `Category` enum 顺序保持 `COMBAT, MOVEMENT, ..., RENDER, ..., MISC`，`fromString` 静态方法的 `equalsIgnoreCase` + 默认返回 `COMBAT` 是 Naven 没有但典型的同源扩展。

### 5.3 设置 / 值系统

**关键证据**：

- 抽象基类 4 个字段一一对应：`name`、`value/currentValue`、`visibility (Supplier<Boolean>)`、子类持有的 `update/onChanged` 回调。
- Naven `Value.isVisible()` 检查 `visibility == null || visibility.get()`；Zen 改名 `SettingVisibility`（仍是 `() -> true` 的 functional interface），构造时 `this.visibility = () -> true`——形状一致。
- `ModeValue / ModeSetting`：都用 `String[]` 存模式列表，都提供"按字符串判断当前模式"的便捷方法（Naven `isCurrentMode`、Zen `is`），`getCurrentMode()` 写成 `values[currentValue]` / `getValue()`。
- `NumberSetting` 字段 `min/max/step` 与 `FloatValue.minValue/maxValue/step` 直接对应；构造参数顺序一致。

### 5.4 命令系统

**关键证据**：

- 命令名、别名一致：`bind / b`、`toggle / t`、`config`、`language`——四条命令的关键字与 Naven 完全相同。
- `Command` 抽象类暴露同样两个抽象方法：`onCommand(String[])` 和 `onTab(String[])`。Naven 用 `@CommandInfo` 注解填字段，Zen 改成构造函数参数，但 `name/aliases` 字段命名一致。
- **提示文案逐字符相同**：`"Bound X to Y."`、`"Unbound X."`、`"Invalid module."`、`"Invalid key."`、`"Usage: .bind <module> [key]"`。
- `onTab` 实现完全相同的一行 stream：`getModules().stream().map(Module::getName).filter(s -> s.toLowerCase().startsWith(args[0].toLowerCase())).toArray(String[]::new)`。
- `CommandManager`：前缀 `.`、匹配后 `cancel/setCancelled`、按空格切分、第一段 toLowerCase 查 `aliasMap`、再用 `System.arraycopy` 切剩余参数——同样结构。

### 5.5 工具类

**关键证据**：

- `ChunkUtil.getLoadedChunks`：与 Naven `ChunkUtils` 几乎逐行相同——`radius = max(2, render distance) + 3`、`min/max ChunkPos`、`Stream.iterate` 的 lambda（`x++ > max.x` 则 `x = min.x; z++`）、**`throw new IllegalStateException("Stream limit didn't work.")`（异常文本完全相同）**、`limit((long) diameter*diameter)`、`filter(hasChunk).map(getChunk).filter(Objects::nonNull)`。
- `BlockUtil`：`canBeClicked(pos)` 返回 `getVoxelShape(pos) != Shapes.empty()`、`getBoundingBox(pos)` 返回 `getVoxelShape(pos).bounds().move(pos)`——同名同实现。
- `RotationUtil` 保留了 Naven 独有的、对工具类而言**非常诡异的 `import org.antlr.v4.runtime.misc.OrderedHashSet`**，并实际使用 `OrderedHashSet<Vec3>`，与 Naven `RotationUtils` 一致。
- "Sensitivity GCD" 公式：Naven `getFixedRotation` 里 `f = sensitivity * 0.6F + 0.2F; gcd = f*f*f*1.2F`。Zen 把它搬到 `Rotation.snapToSensitivity`：`float scaled = sensitivity * 0.6f + 0.2f; float step = scaled*scaled*scaled*1.2f`，数值常量、运算顺序完全相同。
- `diffCalcVector / rotationTo`：都用 `Math.toDegrees(atan2(dz,dx)) - 90.0f` 求 yaw，`-Math.toDegrees(atan2(dy,diffXZ))` 求 pitch，再 `wrapDegrees`——同一公式同一写法。

### 5.6 UI（ClickGui）

**对应关系**：Zen `gui/OldClickGui` + `gui/legacy/*` ≈ Naven `ui/ClickGUI`（视觉风格不同，但同样借助上面 5 个子系统）。

**关键证据**：

- 重写 `Screen` 的同一组生命周期方法。
- `onClose` 调用 `configManager.saveAll()`——与 Naven `ClickGUI` 关闭时通过 `FileManager.save()` 持久化设置的行为对应。
- 按 `Category.values()` 枚举展开面板，构造 `CategoryPanel(x, 20, 140, 20, category)`——20/140 这种典型 GUI 尺寸常数和 Naven 默认布局一致量级。
- `ModuleButton / CategoryPanel / BooleanComponent / ModeComponent / NumberComponent` 的拆分粒度与 Naven 在 `ClickGUI` 单文件内分块渲染时的命名一致。

---

## 总结

OpenZen 的整体架构（事件总线、模块系统、设置系统、命令系统、工具类、ClickGui）几乎完全沿用 Naven 客户端的代码，外加大量同名功能模块。**改动主要集中在重命名、拆分、扩展三件事，核心逻辑、字符串字面量、魔法常数、特征 import 大量保留**——尤其是那个 `RotationUtil` 里完全用不到的 `org.antlr.v4.runtime.misc.OrderedHashSet`、`Stuck` 模块的 `+ 1337`、`Projectiles` 的颜色三元组、`InventoryManager` 的中文 `"点击使用"`、`ChunkUtil` 的 `"Stream limit didn't work."` 异常文案，这些都是无法通过功能重写解释的"抄袭指纹"。

Zen 的反混淆产物在符号层面（类/方法/字段名）经过重新命名，但**字符串字面量层面没有清洗**，这一层是构成抄袭证据最强的源头。
