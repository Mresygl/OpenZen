with open('build.gradle', 'r') as f:
    text = f.read()

text = text.replace('def targetJavaVersion = 21', 'def targetJavaVersion = 21')

with open('build.gradle', 'w') as f:
    f.write(text)
