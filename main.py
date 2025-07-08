import os
import pathlib
import shutil

from gems.gem_world_designer import WorldDesigner

def setup_workspace(zone_name: str) -> pathlib.Path | None:
    """Creates a dedicated directory for the new zone inside the workspace."""
    sanitized_name = "".join(c for c in zone_name if c.isalnum() or c in " _-").lower().replace(" ", "_")
    
    workspace_path = pathlib.Path("workspace")
    zone_path = workspace_path / sanitized_name

    if zone_path.exists():
        print(f"Um workspace para '{zone_name}' já existe")
        overwrite = input("Você gostaria de deletar ele (s/n) ").lower()
        if overwrite == 's':
            print(f"Deletando diretório: {zone_path}")
            shutil.rmtree(zone_path)
        else:
            print("Processo abortado. O workspace não foi criado.")
            return None

    print(f"Criando um novo workspace em: {zone_path}")
    zone_path.mkdir(parents=True, exist_ok=True)
    return zone_path

def main():
    """Main function to orchestrate the MUD creation pipeline."""
    print("--- DeBo Gerador de zonas ---")
    
    zone_name = input("Entre com um nome criativo para a sua nova zona: ")
    if not zone_name:
        print("O nome da zona não pode ser vazio. Abortando.")
        return

    workspace_path = setup_workspace(zone_name)
    if not workspace_path:
        return 
    print(f"\n🗂️ Workspace criado: {workspace_path}"
          )
    concept_brief_path = workspace_path / "0_concept_brief.md"

    print(f"O arquivo de conceito foi criado em: {concept_brief_path}")
    print("Por favor, adicione o conceito criativo da sua zona neste arquivo.")
    
    # Create an empty file for the user to fill
    concept_brief_path.touch()
    
    input("Pressione Enter quando o arquivo estiver pronto para continuar...")

    print("\n🚀 Começando etapa 2: design de mundos..")
    
    try:
        # The 'workspace_path' is passed to the designer so it knows where to read/write files
        world_designer = WorldDesigner(workspace_path)
        success = world_designer.execute_pipeline()

        if success:
            print("\n🎉 O documento de design narrativo está completo!")
        else:
            print("\n🛑 Pipeline foi interrompida pelo usuário durante a criação do documento de desing narrativo.")

    except Exception as e:
        print(f"\nUm erro inesperado ocorreu: {e}")

if __name__ == "__main__":
    main()