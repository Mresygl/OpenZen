with open('.github/workflows/build-loader.yml', 'r') as f:
    text = f.read()

text = text.replace('java-version: 17', 'java-version: 21')

with open('.github/workflows/build-loader.yml', 'w') as f:
    f.write(text)
