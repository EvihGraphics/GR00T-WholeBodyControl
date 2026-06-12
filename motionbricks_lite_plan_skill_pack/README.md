# MotionBricks Lite Plan/Skill Pack

本包是从 `arc_radier_lite` 的组织方式迁移出来的 **MotionBricks Lite 学习复现工程文档包**。

它不是继续 MimicKit ARC Raiders 复现，也不是继续 MimicKit-EvihAnimation mesh parity 计划，而是建立一条新的路线：

```text
MotionBricks 开源仓库环境配置
  -> 预训练 G1 MuJoCo demo 复现
  -> runtime 数据流追踪
  -> synthetic training sanity check
  -> MotionBricks 生成结果导出
  -> EvihAnimation 框架内复现 / 重放 / 可视化
  -> UE5 / MimicKit 后续迁移路线
```

## 使用方式

把本包内容复制到目标仓库根目录，或让 agent 以 `agent_bootstrap_prompt.md` 作为第一条任务指令执行。

建议第一步只读文档，不改代码：

```text
请先读取 docs/skill/motionbricks-*/SKILL.md 与 docs/plan/motionbricks_lite/PLAN-6-11.md，输出你对边界、入口、风险、第一步 smoke test 的理解，然后等待确认。
```

## 重要边界

- 当前 MotionBricks 开源版可以跑 **G1 MuJoCo pretrained interactive demo**。
- 当前训练脚本默认使用 **synthetic random tensor**，只能验证训练链路，不能训练出有语义的走路/爬行/交互模型。
- 当前公开仓库没有 UE5 插件源码。
- EvihAnimation 复现阶段的目标是：把 MotionBricks 生成/导出的 motion buffer 转成 EvihAnimation 可重放的 skeleton/mesh sequence，并输出 PNG、MP4、manifest、review sheet。

## 文档清单

```text
docs/skill/motionbricks-animationtech-skill-v1/SKILL.md
docs/skill/motionbricks-g1-runtime-repro-skill/SKILL.md
docs/skill/motionbricks-training-sanity-skill/SKILL.md
docs/skill/motionbricks-evihanimation-replay-skill/SKILL.md
docs/skill/motionbricks-dashboard-skill/SKILL.md

docs/plan/motionbricks_lite/PLAN-6-11.md
docs/plan/motionbricks_lite/PLAN-6-11-checkpoint-env.md
docs/plan/motionbricks_lite/PLAN-6-11-checkpoint-runtime.md
docs/plan/motionbricks_lite/PLAN-6-11-checkpoint-dataflow.md
docs/plan/motionbricks_lite/PLAN-6-11-checkpoint-training-sanity.md
docs/plan/motionbricks_lite/PLAN-6-11-checkpoint-evihanimation.md

docs/plan/motionbricks_lite/motionbricks_open_source_dataflow.md
docs/plan/motionbricks_lite/motion_representation_notes.md
docs/plan/motionbricks_lite/custom_dataset_bridge_notes.md
docs/plan/motionbricks_lite/evihanimation_replay_contract.md
docs/plan/motionbricks_lite/ue5_mimickit_migration_roadmap.md

templates/*.json
agent_bootstrap_prompt.md
```
