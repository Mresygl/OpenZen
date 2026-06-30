# OpenZen

编译时类名混淆
在执行 \`gradlew build\` 时，\`ext.obfuscateJar\` 会自动把 \`shit.zen.*\` 和 \`asm.patchify.*\` 下的所有类名重命名为随机的 16 位字符，并把原始类名映射保存到 \`build/rename-mapping.txt\` 中。

- 这确保了发布的每个 jar 都是独一无二的
- GitHub Actions \`Build Loader\` 也能自动执行此操作并打包 \`OpenZenLoader.exe\` 和预处理的 DLL。

由于这个构建版本每次产生新的包，如果您担心您的客户端会被按类名特征封禁，请自行拉取源代码构建。
