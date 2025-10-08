import streamlit as st
import sqlite3
import bcrypt
from pages.Comissoes import pagina_comissoes

# ===========================
# Funções auxiliares
# ===========================
def conectar():
    return sqlite3.connect('usuarios.db')

def autenticar(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT senha_hash, nivel FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        senha_hash, nivel = resultado
        if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
            return True, nivel
    return False, None


# ===========================
# Interface de login
# ===========================
def tela_login():
    st.title("🔐 Login do Sistema de Comissões")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        sucesso, nivel = autenticar(usuario, senha)
        if sucesso:
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["nivel"] = nivel
            st.success(f"Bem-vindo(a), {usuario}! 🚀")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos ❌")


# ===========================
# Página principal
# ===========================
def main():
    if "logado" not in st.session_state or not st.session_state["logado"]:
        tela_login()
    else:
        st.sidebar.title("Menu")
        st.sidebar.write(f"👤 Usuário: {st.session_state['usuario']}")
        st.sidebar.write(f"🧩 Nível: {st.session_state['nivel']}")

        menu = st.sidebar.radio("Navegar para:", ["📊 Comissões", "👥 Gerenciar Usuários", "🚪 Sair"])

        if menu == "📊 Comissões":
            pagina_comissoes()

        elif menu == "👥 Gerenciar Usuários":
            if st.session_state["nivel"] == "admin":
                from pages.Gerenciar_Usuarios import gerenciar_usuarios
                gerenciar_usuarios()
            else:
                st.warning("⚠️ Acesso restrito a administradores.")

        elif menu == "🚪 Sair":
            for key in ["logado", "usuario", "nivel"]:
                st.session_state.pop(key, None)
            st.experimental_rerun()


if __name__ == "__main__":
    main()
