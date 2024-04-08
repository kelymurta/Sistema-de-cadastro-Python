#!/usr/bin/env python
# coding: utf-8

# ### Aqui estão as funções que constroem a interface gráfica no Streamlit

# Streamlit é uma biblioteca Python de código aberto qque combina recursos poderosos de visualização com a simplicidade da sintaxe do Python. O Streamlit permite criar aplicativos da Web rapidamente. 

# In[ ]:


import streamlit as st
import json

def lerArquivos():
    with open("projetoModuloII.json", "r") as f:

        data = json.load(f)
    return data

def inserirUsuarios(arquivo):
    #dadois de usuarios inseridos vem pra cá depois são salvos
    usuarios_adicionados = st.session_state.get("usuarios_adicionados", [])

    nome = st.text_input("Por favor, insira o nome do usuário:")
    telefone = st.text_input("Por favor, insira o telefone do usuário:")
    endereco = st.text_input("Por favor, insira o endereço do usuário:")

    # um botão para finalizar e adicionar no dict
    if st.button("Adicionar Usuário Completo"):

        nome = nome if nome else "Não informado"
        telefone = telefone if telefone else "Não informado"
        endereco = endereco if endereco else "Não informado"

        ID = str(len(arquivo) + 1) #isso aqui vai ser o ID de cada usuário
        status = True  # Valor default para o status

        # verificando se o usuário existe no sistema
        usuario_existente = None
        for chave, usuario in arquivo.items():
            if usuario["Nome"] == nome and usuario["Telefone"] == telefone and usuario["Endereço"] == endereco:
                usuario_existente = chave
                break

        if usuario_existente:
            # se existe, ele vira True, apenas
            arquivo[usuario_existente]["Status"] = True
        else:
            #se não existe, é adicionado
            novo_usuario = {
                "Status": status,
                "Nome": nome,
                "Telefone": telefone,
                "Endereço": endereco
            }
            arquivo[ID] = novo_usuario
            st.success("Usuário adicionado com sucesso.")


        try:
            with open("projetoModuloII.json", 'w', encoding='utf-8') as file:
                json.dump(arquivo, file, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Erro ao salvar o arquivo: {str(e)}")
    
def excluirUsuarios(arquivos):
    
    entrada = st.text_input("Digite um ID:")
    #de acordo com a existencia do ID ele coloca o status como False ou pede um ID válido
    if entrada in arquivos:
        arquivos[entrada]["Status"] = False
        with open("projetoModuloII.json", 'w', encoding='utf-8') as file:
            json.dump(arquivos, file, indent=2, ensure_ascii= False)
    else:
        st.warning("ID inválido. Tente novamente.")
        
        
def acessarInfos(arquivo):    

        #pede o id
        idVisualizar = st.text_input("Digite o ID do usuário para visualizar seus dados: ")
        
        #de acordo com a existencia do ID ele mostra as informações ou fala que o ID tá invalido
        if idVisualizar in arquivo:
            usuario = arquivo[idVisualizar]
            st.write(f"\nNome: {usuario['Nome']}\n\nTelefone: {usuario['Telefone']}\n\nEndereço: {usuario['Endereço']}")
        else:
            st.warning("ID inválido. Tente novamente.")    


def exibirInfos(arquivo):
    
    #aqui acesso as informações de todos os usuarios
    for chave, usuario in arquivo.items():
        info_usuario = (
            f"ID: {chave}\n\n"
            f"Nome: {usuario['Nome']}\n\n"
            f"Telefone: {usuario['Telefone']}\n\n"
            f"Endereço: {usuario['Endereço']}\n\n"
        )
        #e aqui é o "print" do streamlit
        st.write(info_usuario)
    try:
            with open("projetoModuloII.json", 'w', encoding='utf-8') as file:
                json.dump(arquivo, file, indent=2, ensure_ascii= False)
    except:
            st.error("Deu errado, não salvou.")
            
def atualizarInfos(arquivo):
        
        #esse st.markdown é um "print" arrumadinho
        st.markdown("<h3 style='color: white;'>Digite o ID do usuário que deseja fazer alteração:</h3>", unsafe_allow_html=True)
        idAlterar = st.text_input("") #input do id pra atualizar

        #aqui o usuario escolhe qual informação atualizar
        if idAlterar in arquivo:
            st.markdown("<h3 style='color: white;'>Qual informação você gostaria de fazer uma alteração?</h3>", unsafe_allow_html=True)
            st.markdown("<h5 style='color: white;'>Por favor, escolha uma opção numérica: \n\n[1] Nome [2] Telefone [3] Endereço</h5>", unsafe_allow_html=True)
            entrada1 = st.number_input("", format="%.0f")

            if entrada1 == 1:
                nomeNovo = st.text_input("Digite o novo nome do usuário: ")
                arquivo[idAlterar]["Nome"]=nomeNovo

            elif entrada1 == 2:
                telefoneNovo = st.number_input("Digite o novo telefone do usuário: ", format="%.0f")
    
                arquivo[idAlterar]["Telefone"]=telefoneNovo

            elif entrada1 == 3:
                enderecoNovo = st.text_input("Digite o novo endereço do usuário: ")
                arquivo[idAlterar]["Endereço"]=enderecoNovo
                
            else: 
                if entrada1 != 3 and entrada1 != 2 and entrada1 != 1 and entrada1 != 0: 
                    st.warning("Opção inválida. Tente novamente.") 
                    
        #se o id não é válido:
        else:
            if idAlterar not in arquivo:
                st.warning("ID inválido. Tente novamente.")
        
        try:
            with open("projetoModuloII.json", 'w', encoding='utf-8') as file:
                json.dump(arquivo, file, indent=2, ensure_ascii= False)
        except: "Deu errado, não salvou."
            
        
def main():


    #caixa de seleção para selecionar a opção e executar
    escolha = st.sidebar.selectbox("Escolha uma opção", ["Inserir usuários", "Excluir usuários", "Atualizar informações de usuários",                                        "Acessar informações de um usuário", "Acessar informações de todos os usuários",                                        "Sair do sistema"])
    
    if escolha == "Inserir usuários":
        opcao1()
    elif escolha == "Excluir usuários":
        opcao2()
    elif escolha == "Atualizar informações de usuários":
        opcao3()
    elif escolha == "Acessar informações de um usuário":
        opcao4()
    elif escolha == "Acessar informações de todos os usuários":
        opcao5()
    elif escolha == "Sair do sistema":
        opcao6()

#de acordo com a opção, eu chamo a função
def opcao1():
    st.markdown("<h1 text-align: center; style='color: red;'>Seja bem vindo ao sistema de cadastro do iFood!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 text-align: center; style='color: red;'>Você escolheu a opção de inserir um novo usuário.</h2>", unsafe_allow_html=True)

    inserirUsuarios(lerArquivos())

def opcao2():
    st.markdown("<h1 text-align: center; style='color: red;'>Seja bem vindo ao sistema de cadastro do iFood!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 text-align: center; style='color: red;'>Você escolheu a opção de excluir um usuário.</h2>", unsafe_allow_html=True)

    excluirUsuarios(lerArquivos())
    
def opcao3():
    st.markdown("<h1 text-align: center; style='color: red;'>Seja bem vindo ao sistema de cadastro do iFood!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 text-align: center; style='color: red;'>Você escolheu a opção de atualizar dados de um usuário.</h2>", unsafe_allow_html=True)

    atualizarInfos(lerArquivos())

def opcao4():
    st.markdown("<h1 text-align: center; style='color: red;'>Seja bem vindo ao sistema de cadastro do iFood!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 text-align: center; style='color: red;'>Você escolheu a opção de acessar as informações de um usuário do sistema.</h2>", unsafe_allow_html=True)

    acessarInfos(lerArquivos())

def opcao5():
    st.markdown("<h1 text-align: center; style='color: red;'>Seja bem vindo ao sistema de cadastro do iFood!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 text-align: center; style='color: red;'>Você escolheu a opção de visualizar os dados de todos os usuários do sistema.</h2>", unsafe_allow_html=True)
    exibirInfos(lerArquivos())

def opcao6():
    st.markdown("<h1 text-align: center; style='color: red;'>Você escolheu a opção de sair do sistema, o iFood agradece a sua visita. </h1>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()

