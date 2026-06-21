import { useState, useRef, useEffect } from "react";
import {
  Send, Bot, User, Leaf, Sprout, CloudRain, Bug, RotateCcw,
} from "lucide-react";
import { envoyerMessage } from "../services/api";

const suggestions = [
  { icon: <Bug size={14} />,       texte: "Comment prévenir le mildiou sur les tomates ?" },
  { icon: <CloudRain size={14} />, texte: "Quel est l'impact de la pluie sur mes récoltes ?" },
  { icon: <Sprout size={14} />,    texte: "Quand planter les oignons au Sénégal ?" },
  { icon: <Leaf size={14} />,      texte: "Quels engrais utiliser pour les carottes ?" },
];

const messagesInitiaux = [
  {
    id:    1,
    role:  "assistant",
    texte: "Bonjour ! Je suis votre assistant agricole IA 🌱\n\nJe peux vous aider avec :\n• Le diagnostic et traitement des maladies\n• Les conseils de plantation et récolte\n• La gestion de vos cultures\n• Les pratiques agricoles adaptées au Sénégal\n\nComment puis-je vous aider aujourd'hui ?",
    heure: "09:00",
  },
];

const Message = ({ msg }) => {
  const isUser = msg.role === "user";
  return (
    <div className={`flex items-end gap-2.5 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
      <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 ${isUser ? "bg-primary" : "bg-[#102215]"}`}>
        {isUser ? <User size={14} className="text-[#102215]" /> : <Bot size={14} className="text-primary" />}
      </div>
      <div className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-line ${
        isUser
          ? "bg-primary text-[#102215] font-medium rounded-br-sm"
          : "bg-white border border-gray-100 text-gray-700 rounded-bl-sm shadow-sm"
      }`}>
        {msg.texte}
        <p className={`text-xs mt-1.5 ${isUser ? "text-[#102215]/50 text-right" : "text-gray-300"}`}>
          {msg.heure}
        </p>
      </div>
    </div>
  );
};

const ConseilIA = () => {
  const [messages, setMessages] = useState(messagesInitiaux);
  const [input, setInput]       = useState("");
  const [loading, setLoading]   = useState(false);
  const bottomRef               = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const getHeure = () => new Date().toLocaleTimeString("fr-FR", {
    hour: "2-digit", minute: "2-digit"
  });

  const envoyer = async (texte) => {
    if (!texte.trim() || loading) return;

    const msgUser = {
      id: Date.now(), role: "user", texte: texte.trim(), heure: getHeure()
    };
    setMessages(prev => [...prev, msgUser]);
    setInput("");
    setLoading(true);

    try {
      // Appel réel au backend
      const res = await envoyerMessage({
        message: texte.trim(),
        culture: ""
      });
      // Simulation d'un délai de réflexion pour rendre l'IA plus crédible
      setTimeout(() => {
        const msgIA = {
          id:    Date.now() + 1,
          role:  "assistant",
          texte: res.data.reponse,
          heure: getHeure(),
        };
        setMessages(prev => [...prev, msgIA]);
        setLoading(false);
      }, 1500);
      return; // Empêcher le passage au finally immédiat
    } catch {
      const msgErreur = {
        id:    Date.now() + 1,
        role:  "assistant",
        texte: "Désolé, je rencontre une difficulté. Veuillez réessayer.",
        heure: getHeure(),
      };
      setMessages(prev => [...prev, msgErreur]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      envoyer(input);
    }
  };

  const reinitialiser = () => setMessages(messagesInitiaux);

  return (
    <div className="flex flex-col gap-4 max-w-3xl mx-auto">

      {/* En-tête */}
      <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 bg-[#102215] rounded-xl flex items-center justify-center">
            <Bot size={22} className="text-primary" />
          </div>
          <div>
            <h2 className="text-gray-800 font-semibold text-base">Assistant Conseil IA</h2>
            <div className="flex items-center gap-1.5 mt-0.5">
              <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
              <span className="text-xs text-gray-400">En ligne — Prêt à vous conseiller</span>
            </div>
          </div>
        </div>
        <button
          onClick={reinitialiser}
          className="flex items-center gap-2 px-3 py-2 rounded-xl border border-gray-200 text-gray-500 text-xs hover:bg-gray-50 transition-colors"
        >
          <RotateCcw size={13} /> Nouvelle conversation
        </button>
      </div>

      {/* Zone chat */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm flex flex-col" style={{ height: "460px" }}>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-4">
          {messages.map((msg) => <Message key={msg.id} msg={msg} />)}

          {/* Indicateur frappe */}
          {loading && (
            <div className="flex items-end gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-[#102215] flex items-center justify-center shrink-0">
                <Bot size={14} className="text-primary" />
              </div>
              <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t border-gray-100">
          <div className="flex items-end gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Posez votre question agricole..."
              rows={1}
              className="flex-1 resize-none bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-700 outline-none focus:border-primary focus:bg-white transition-all placeholder:text-gray-400"
            />
            <button
              onClick={() => envoyer(input)}
              disabled={!input.trim() || loading}
              className={`w-11 h-11 rounded-xl flex items-center justify-center transition-all shrink-0 ${
                input.trim() && !loading
                  ? "bg-primary text-[#102215] hover:opacity-90 shadow-md"
                  : "bg-gray-100 text-gray-400 cursor-not-allowed"
              }`}
            >
              <Send size={16} />
            </button>
          </div>
          <p className="text-xs text-gray-300 mt-2 text-center">
            Entrée pour envoyer · Shift+Entrée pour sauter une ligne
          </p>
        </div>
      </div>

      {/* Suggestions */}
      <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
        <p className="text-xs text-gray-400 font-medium mb-3 uppercase tracking-wide">
          Questions fréquentes
        </p>
        <div className="grid grid-cols-2 gap-2">
          {suggestions.map((s, i) => (
            <button
              key={i}
              onClick={() => envoyer(s.texte)}
              className="flex items-center gap-2 px-3 py-2.5 rounded-xl border border-gray-100 bg-gray-50 text-xs text-gray-600 hover:border-primary/30 hover:bg-primary/5 hover:text-primary transition-all text-left"
            >
              <span className="text-primary shrink-0">{s.icon}</span>
              {s.texte}
            </button>
          ))}
        </div>
      </div>

    </div>
  );
};

export default ConseilIA;