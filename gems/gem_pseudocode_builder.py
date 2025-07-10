import pathlib
import config 
from google import genai
from google.genai import types

class PseudocodeBuilder:
    """
    Facilitates the generation of pseudocode for game mechanics and systems.
    """
    def __init__(self, workspace_path: pathlib.Path):
        """
        Initializes the PseudocodeBuilder, configures the Gemini API client,
        and loads the system prompt.
        """
        print("Pseudocode Builder iniciado...")
        self.workspace_path = workspace_path
        self.narrative_doc_path = workspace_path / "1_narrative_design.md"
        self.pseudocode_doc_path = workspace_path / "2_pseudocode.md"

        try:
            self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        except AttributeError:
            raise ValueError("GEMINI_API_KEY não está carregada corretamente. Verifique seu arquivo .env.")

        # Load the main instruction file for this Gem
        instruction_path = pathlib.Path("instructions/pseudocode_builder.xml")

        self.model = "gemini-2.5-pro"
        try:
            self.system_prompt = instruction_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            raise FileNotFoundError(f"Erro crítico: arquivo de instruções não encontrado {instruction_path}")
        
        self.config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction = [types.Part.from_text(text=self.system_prompt)]
        )

        print("Gemini Model configurado com sucesso.")
        
        # Initialize an empty pseudocode document file
        self.pseudocode_doc_path.touch()

    def _call_gemini_api(self, prompt: str, file) -> str:
            """
            Sends a prompt to the Gemini API and returns the complete response text.
            """
            print("\n[--- Requisitando Gemini API... ---]")
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[prompt, file],
                    config=self.config
                )

                print("[--- Chamada completa Complete ---]\n")
                return response.text or "Erro: A resposta da API estava vazia."
            except Exception as e:
                # Handle potential API errors gracefully
                print(f"Um erro ocorreu na chamada da API: {e}")
                return f"Erro: Nao foi prossivel gerar. Detalhes: {e}"

    def generate_pseudocode(self) -> bool:
            """
            Generates pseudocode based
            """
            print("\n[--- Gerando Pseudocode... ---]")
            try:
                prompt = "Por favor, gere pseudocode para o seguinte design narrativo:\n\n"
                prompt += self.narrative_doc_path.read_text(encoding='utf-8')
                
                script_dir = pathlib.Path(__file__).parent.parent # Go up from gems/ to the root
                pdf_path = script_dir / "building.pdf"

                if not pdf_path.exists():
                    raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")
                
                file = self.client.files.upload(file=pdf_path)
                if not file:
                    raise ValueError("Erro ao carregar o arquivo PDF.")
                
                response_text = self._call_gemini_api(prompt,file)

                self.pseudocode_doc_path.write_text(response_text, encoding='utf-8')

                print("Pseudocode gerado e salvo com sucesso.")
                return True
            except Exception as e:
                print(f"Erro ao gerar pseudocode: {e}")
                return False