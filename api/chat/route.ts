import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! });

// Sett denne til ID-en til vector store du opprettet ved opplasting
const VECTOR_STORE_ID = process.env.OPENAI_VECTOR_STORE_ID!;

export async function POST(req: Request) {
  const { message } = await req.json();

  const response = await client.responses.create({
    model: "gpt-4.1-mini",
    input: [
      {
        role: "system",
        content:
          "Du er talsperson for et fiktivt parti. Svar kun basert på partiprogrammet. " +
          "Hvis programmet ikke dekker spørsmålet, si det tydelig og foreslå nærmeste relevante tema. " +
          "Ikke finn på standpunkt, tall eller detaljer."
      },
      { role: "user", content: message }
    ],
    tools: [
      {
        type: "file_search",
        vector_store_ids: [VECTOR_STORE_ID]
      }
    ]
  });

  // Enkelt uttrekk av tekstsvar (UI kan bygges mer robust senere)
  const text = response.output_text;

  return Response.json({ answer: text });
}
