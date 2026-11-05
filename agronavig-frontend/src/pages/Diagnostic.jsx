import { useState, useRef } from "react";
import { Upload, ImagePlus, X, FlaskConical, Leaf, Camera } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { analyserImage } from "../services/api";

const cultures = [
  { value: "Apple",      label: "Pommier",   emoji: "🍎" },
  { value: "Cherry",     label: "Cerisier",  emoji: "🍒" },
  { value: "Corn",       label: "Maïs",      emoji: "🌽" },
  { value: "Grape",      label: "Vigne",     emoji: "🍇" },
  { value: "Orange",     label: "Oranger",   emoji: "🍊" },
  { value: "Peach",      label: "Pêcher",    emoji: "🍑" },
  { value: "Pepper",     label: "Poivron",   emoji: "🫑" },
  { value: "Potato",     label: "P. de terre", emoji: "🥔" },
  { value: "Squash",     label: "Courge",    emoji: "🎃" },
  { value: "Strawberry", label: "Fraisier",  emoji: "🍓" },
  { value: "Tomato",     label: "Tomate",    emoji: "🍅" },
  { value: "Soybean",    label: "Soja",      emoji: "🫘" },
];

const Diagnostic = () => {
  const [image, setImage]       = useState(null);
  const [preview, setPreview]   = useState(null);
  const [culture, setCulture]   = useState("");
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading]   = useState(false);
  const inputRef                = useRef(null);
  const navigate                = useNavigate();

  const handleImage = (file) => {
    if (!file || !file.type.startsWith("image/")) return;
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleImage(e.dataTransfer.files[0]);
  };

  const removeImage = () => {
    setImage(null);
    setPreview(null);
  };

  const handleAnalyse = async () => {
    if (!image || !culture) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("culture", culture);
      formData.append("file", image);
      const res = await analyserImage(formData);
      localStorage.setItem("dernierDiagnostic", JSON.stringify(res.data));
      navigate("/diagnostic/resultat");
    } catch (err) {
      const detail = err.response?.data?.detail;
      const message = detail || (!err.response
        ? "Le backend FastAPI est inaccessible. Vérifiez qu'il fonctionne sur http://127.0.0.1:8000."
        : "Le serveur n'a pas pu analyser cette image. Consultez le terminal backend.");
      alert(`Erreur lors de l'analyse : ${message}`);
    } finally {
      setLoading(false);
    }
  };

  const pret = image && culture;

  return (
    <div className="flex flex-col gap-6 max-w-4xl mx-auto">

      {/* En-tête */}
      <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 bg-primary/10 rounded-xl flex items-center justify-center">
            <FlaskConical size={22} className="text-primary" />
          </div>
          <div>
            <h2 className="text-gray-800 font-semibold text-lg">Diagnostic des maladies</h2>
            <p className="text-gray-400 text-sm">Uploadez une photo de votre culture pour détecter les maladies par IA</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Zone upload */}
        <div className="flex flex-col gap-4">
          <div
            className={`relative border-2 border-dashed rounded-2xl transition-all duration-200 cursor-pointer
              ${dragging ? "border-primary bg-primary/5 scale-[1.01]" : "border-gray-200 bg-white hover:border-primary/50 hover:bg-gray-50"}
              ${preview ? "p-0 overflow-hidden" : "p-10"}
            `}
            onClick={() => !preview && inputRef.current.click()}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
          >
            {preview ? (
              <>
                <img src={preview} alt="Aperçu" className="w-full h-72 object-cover rounded-2xl" />
                <button
                  onClick={(e) => { e.stopPropagation(); removeImage(); }}
                  className="absolute top-3 right-3 w-8 h-8 bg-red-500 rounded-full flex items-center justify-center hover:bg-red-600 transition-colors shadow-md"
                >
                  <X size={14} className="text-white" />
                </button>
              </>
            ) : (
              <div className="flex flex-col items-center gap-4 text-center">
                <div className="w-20 h-20 bg-primary/10 rounded-3xl flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Camera size={32} className="text-primary lg:hidden" />
                  <ImagePlus size={32} className="text-primary hidden lg:block" />
                </div>
                <div>
                  <p className="text-gray-700 font-bold text-base lg:hidden">Prendre une photo</p>
                  <p className="text-gray-700 font-bold text-base hidden lg:block">Glissez une image ici</p>
                  <p className="text-gray-400 text-xs mt-1">Formats supportés : JPG, PNG, WEBP</p>
                </div>
                <div className="flex items-center gap-2 mt-1">
                  <span className="lg:hidden text-xs bg-[#102215] text-white px-4 py-2 rounded-xl font-medium">Ouvrir l'appareil photo</span>
                  <span className="hidden lg:block text-xs bg-gray-100 text-gray-500 px-4 py-2 rounded-xl font-medium">Parcourir les fichiers</span>
                </div>
              </div>
            )}
          </div>
          <input
            ref={inputRef}
            type="file"
            accept="image/*"
            capture="environment"
            className="hidden"
            onChange={(e) => handleImage(e.target.files[0])}
          />

          {image && (
            <div className="flex items-center gap-3 bg-green-50 border border-green-100 rounded-xl px-4 py-3">
              <Upload size={15} className="text-green-500" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-green-700 truncate">{image.name}</p>
                <p className="text-xs text-green-400">{(image.size / 1024).toFixed(1)} KB</p>
              </div>
              <span className="text-xs bg-green-100 text-green-600 px-2 py-0.5 rounded-full font-medium">Prêt</span>
            </div>
          )}
        </div>

        {/* Sélection culture + bouton */}
        <div className="flex flex-col gap-4">
          <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <Leaf size={16} className="text-primary" />
              <h3 className="text-gray-700 font-semibold text-sm">Sélectionner la culture</h3>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {cultures.map((c) => (
                <button
                  key={c.value}
                  onClick={() => setCulture(c.value)}
                  className={`flex items-center gap-2 px-3 py-2.5 rounded-xl border text-sm font-medium transition-all duration-150
                    ${culture === c.value
                      ? "border-primary bg-primary/10 text-primary"
                      : "border-gray-100 bg-gray-50 text-gray-600 hover:border-primary/30 hover:bg-primary/5"
                    }`}
                >
                  <span>{c.emoji}</span>
                  {c.label}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleAnalyse}
            disabled={!pret || loading}
            className={`w-full py-4 rounded-2xl font-semibold text-sm flex items-center justify-center gap-2 transition-all duration-200
              ${pret && !loading
                ? "bg-primary text-[#102215] hover:opacity-90 shadow-md hover:shadow-lg"
                : "bg-gray-100 text-gray-400 cursor-not-allowed"
              }`}
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-[#102215]/30 border-t-[#102215] rounded-full animate-spin" />
                Analyse en cours...
              </>
            ) : (
              <>
                <FlaskConical size={16} />
                Lancer l'analyse IA
              </>
            )}
          </button>

          {!pret && (
            <div className="bg-blue-50 border border-blue-100 rounded-xl px-4 py-3">
              <p className="text-xs text-blue-500 font-medium">💡 Pour lancer l'analyse :</p>
              <ul className="text-xs text-blue-400 mt-1 flex flex-col gap-0.5">
                {!image   && <li>• Uploadez une photo de la plante</li>}
                {!culture && <li>• Sélectionnez le type de culture</li>}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Diagnostic;