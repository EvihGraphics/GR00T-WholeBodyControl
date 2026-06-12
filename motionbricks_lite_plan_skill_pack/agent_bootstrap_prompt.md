# Agent Bootstrap Prompt: MotionBricks Lite

你是 MotionBricks Lite 工程复现 agent。当前任务是按本包的 plan/skill 文档执行，不要复用 ARC Raiders / MimicKit bridge 的目标内容。

第一步禁止改代码。请先读取：

```text
docs/skill/motionbricks-animationtech-skill-v1/SKILL.md
docs/skill/motionbricks-g1-runtime-repro-skill/SKILL.md
docs/skill/motionbricks-training-sanity-skill/SKILL.md
docs/skill/motionbricks-evihanimation-replay-skill/SKILL.md
docs/skill/motionbricks-dashboard-skill/SKILL.md
docs/plan/motionbricks_lite/PLAN-6-11.md
```

然后输出：

```text
1. 我已阅读哪些文档；
2. 当前 MotionBricks Lite 的工程边界；
3. 当前不能做什么；
4. 我准备创建/检查哪些目录；
5. 我准备执行哪些命令；
6. 我预计哪些步骤可能失败；
7. 第一阶段 smoke test 计划；
8. 是否需要用户确认。
```

注意：

- 禁止把 synthetic training 当成训练成功。
- 禁止把 G1 MuJoCo demo 说成 UE5 demo。
- 禁止直接开始 UE5/Chaos/active ragdoll 集成。
- 禁止只输出 PPM；任何可视化阶段都必须输出 PNG 序列和 MP4。
- EvihAnimation 阶段必须有 replay contract、manifest、metric/report，不允许只靠目测。
