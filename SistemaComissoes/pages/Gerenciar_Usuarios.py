import streamlit as st
import sqlite3
import bcrypt

def conectar():
    return sqlite3.connect('usuarios.db')

def gerenciar_usuarios():
    st.title("👥 Gerenciar Usuários")

    # Formulário para adicionar usuário
    st.subheader("➕ Adicionar novo usuário")
    nome = st.text_input("Nome completo")
    usuario = st.text_input("Usuário (login)")
    senha = st.text_input("Senha", type="password")
    nivel = st.selectbox("Nível de acesso", ["admin", "colaborador"])

    if st.button("Salvar usuário"):
        if nome and usuario and senha:
            conn = conectar()
            cursor = conn.cursor()
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            try:
                cursor.execute('''
                    INSERT INTO usuarios (nome, usuario, senha_hash, nivel)
                    VALUES (?, ?, ?, ?)
                ''', (nome, usuario, senha_hash, nivel))
                conn.commit()
                st.success(f"Usuário '{usuario}' criado com sucesso ✅")
            except sqlite3.IntegrityError:
                st.error("❌ Usuário já existe!")
            conn.close()
        else:
            st.warning("Preencha todos os campos!")

    # Listar usuários
    st.subheader("📋 Lista de usuários cadastrados")
    conn = conectar()
    usuarios = conn.execute("SELECT id, nome, usuario, nivel FROM usuarios").fetchall()
    conn.close()

    if usuarios:
        for u in usuarios:
            st.write(f"🧍‍♂️ ID: {u[0]} | Nome: {u[1]} | Usuário: {u[2]} | Nível: {u[3]}")
    else:
        st.info("Nenhum usuário cadastrado ainda.")
