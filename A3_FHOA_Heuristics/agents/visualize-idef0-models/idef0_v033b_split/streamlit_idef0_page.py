import streamlit as st
st.set_page_config(layout='wide', page_title='IDEF0 Diagrammer v0.3.3b')
st.title('IDEF0 Diagrammer v0.3.3b')

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

html = read('index.html').replace('href="styles.css"', '<style>'+read('styles.css')+'</style>')                          .replace('<script src="app.js"></script>', '<script>'+read('app.js')+'</script>')
st.components.v1.html(html, height=800, scrolling=True)
