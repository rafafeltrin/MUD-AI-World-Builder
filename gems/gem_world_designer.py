import pathlib
import config 
from google import genai
from google.genai import types

class WorldDesigner:
    """
    Orchestrates the interactive, multi-stage narrative design process.
    """
    def __init__(self, workspace_path: pathlib.Path):
        """
        Initializes the WorldDesigner, configures the Gemini API client,
        and loads the system prompt.
        """
        print("Design de mundos iniciado...")
        self.workspace_path = workspace_path
        self.concept_brief_path = workspace_path / "0_concept_brief.md"
        self.narrative_doc_path = workspace_path / "1_narrative_design.md"

        try:
            self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        except AttributeError:
            raise ValueError("GEMINI_API_KEY não está carregada corretamente. Verifique seu arquivo .env.")

        # Load the main instruction file for this Gem
        instruction_path = pathlib.Path("instructions/world_designer.xml")

        try:
            self.system_prompt = instruction_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            raise FileNotFoundError(f"Erro crítico: arquivo de instruções não encontrado {instruction_path}")
        
        # Configure the model with the system instructions
        self.model = "gemini-2.5-pro"

        self.config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction = [types.Part.from_text(text=self.system_prompt)]
        )

        print("Gemini Model configurado com sucesso.")
        
        # Initialize an empty narrative document file
        self.narrative_doc_path.touch()


    def _call_gemini_api(self, prompt: str) -> str:
        """
        Sends a prompt to the Gemini API and returns the complete response text.
        """
        print("\n[--- Requisitando Gemini API... ---]")
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=self.config
            )

            print("[--- Chamada completa Complete ---]\n")
            return response.text or "Erro: A resposta da API estava vazia."
        except Exception as e:
            # Handle potential API errors gracefully
            print(f"Um erro ocorreu na chamada da API: {e}")
            return f"Erro: Nao foi prossivel gerar. Detalhes: {e}"


    def _get_user_feedback(self) -> tuple[bool, str | None]:
        """
        Prompts the user for approval or feedback.
        Returns a tuple: (is_approved, feedback_text).
        """
        while True:
            answer = input("Você aprova essa seção? (s/n): ").lower()
            if answer == "s":
                return True, None
            if answer == "n":
                feedback = input("Por favor escreva um feadback para revisão: ")
                return False, feedback
            print("Entrada inválida. Por favor entre com 's' or 'n'.")

    def _run_stage_1_map(self) -> bool:
        """
        Executes the generation and revision loop for Stage 1 (Map & Overview).
        """
        print("\n--- Começando a etapa 1: Gerando um overview geral e um para conceitual ---")
        concept = self.concept_brief_path.read_text()
        current_prompt = f"""
        CONCEPT BRIEF:
        {concept}
        ---
        ACTION: Execute STAGE 1: General Overview and Conceptual Map. Your output should only be the content for Section 1 of 
        the Narrative Design Document.
        """
        
        while True:
            generated_content = self._call_gemini_api(current_prompt)
            print("--- Generated Content ---\n" + generated_content)
            
            is_approved, feedback = self._get_user_feedback()
            
            if is_approved:
                self.narrative_doc_path.write_text(generated_content)
                print("Estágio 1 concluído com sucesso! O conteúdo foi salvo no documento.")
                return True
            
            print("--- Revisando o prompt com o seu feedback ---")
            current_prompt = f"""
            PREVIOUSLY GENERATED CONTENT (REJECTED):
            {generated_content}
            ---
            USER FEEDBACK FOR REVISION:
            {feedback}
            ---
            ACTION: Regenerate the content for Section 1 of the Narrative Design Document, considering the user's feedback.
            """
    
    def _run_stage_2_rooms(self) -> bool:
        print("\n--- Começando a etapa 2: Detalhe das salas  ---")

        return True

    def _run_stage_3_creatures(self) -> bool:
        print("\n--- (Placeholder) Stage 3: Creature & NPC Dossier ---")
        return True

    def _run_stage_4_items(self) -> bool:
        print("\n--- (Placeholder) Stage 4: Item & Treasure Catalog ---")
        return True

    def execute_pipeline(self) -> bool:
        """
        Runs the full, multi-stage design process, stopping if any stage fails or is aborted.
        """
        if not self._run_stage_1_map(): return False
        if not self._run_stage_2_rooms(): return False
        if not self._run_stage_3_creatures(): return False
        if not self._run_stage_4_items(): return False
        
        return True