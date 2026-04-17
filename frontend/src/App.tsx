import { useEffect, useMemo, useState } from "react";
import axios from "axios";

type RecommendationRequest = {
  citizenship: string;
  purpose_of_entry: string;
  entry_date: string;
  stay_duration_days: number;
  has_insurance: boolean;
  employment_related: boolean;
};

type RequirementItem = {
  code: string;
  title: string;
  required: boolean;
  deadline?: string | null;
  place?: string | null;
  reason: string;
};

type RecommendationResponse = {
  profile: RecommendationRequest;
  requirements: RequirementItem[];
  summary: {
    required_count: number;
    optional_count: number;
  };
};

type HistoryItem = {
  id: number;
  citizenship: string;
  purpose_of_entry: string;
  entry_date: string;
  stay_duration_days: number;
  has_insurance: boolean;
  employment_related: boolean;
  medical_required: boolean;
  insurance_required: boolean;
  created_at: string;
};

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

const initialForm: RecommendationRequest = {
  citizenship: "",
  purpose_of_entry: "трудовая деятельность",
  entry_date: "",
  stay_duration_days: 90,
  has_insurance: false,
  employment_related: true,
};

export default function App() {
  const [form, setForm] = useState<RecommendationRequest>(initialForm);
  const [result, setResult] = useState<RecommendationResponse | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [countries, setCountries] = useState<string[]>([]);
  const [purposes, setPurposes] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadRefs() {
    const [countriesRes, purposesRes, historyRes] = await Promise.all([
      api.get("/reference/countries"),
      api.get("/reference/purposes"),
      api.get("/history"),
    ]);
    setCountries(countriesRes.data.policy_countries || []);
    setPurposes(purposesRes.data.purposes || []);
    setHistory(historyRes.data || []);
  }

  useEffect(() => {
    loadRefs().catch(() => setError("Не удалось загрузить справочные данные"));
  }, []);

  const canSubmit = useMemo(() => {
    return (
      form.citizenship.trim() !== "" &&
      form.purpose_of_entry.trim() !== "" &&
      form.entry_date.trim() !== "" &&
      Number.isFinite(form.stay_duration_days) &&
      form.stay_duration_days > 0
    );
  }, [form]);

  async function submitForm(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const response = await api.post<RecommendationResponse>("/recommendations", form);
      setResult(response.data);
      const historyRes = await api.get("/history");
      setHistory(historyRes.data || []);
    } catch {
      setError("Не удалось сформировать рекомендации");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="hero">
        <div>
          <h1>Медицинские требования иностранного гражданина</h1>
          <p>
            Веб-сервис определяет необходимость медицинского освидетельствования
            и оформления полиса по выбранным правилам дорожной карты.
          </p>
        </div>
      </header>

      <main className="layout">
        <section className="card">
          <h2>Анкета</h2>
          <form onSubmit={submitForm} className="form">
            <label>
              Гражданство
              <input
                type="text"
                value={form.citizenship}
                onChange={(e) => setForm({ ...form, citizenship: e.target.value })}
                placeholder="Например, Узбекистан"
              />
            </label>

            <label>
              Цель въезда
              <select
                value={form.purpose_of_entry}
                onChange={(e) => setForm({ ...form, purpose_of_entry: e.target.value })}
              >
                {purposes.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Дата въезда
              <input
                type="date"
                value={form.entry_date}
                onChange={(e) => setForm({ ...form, entry_date: e.target.value })}
              />
            </label>

            <label>
              Срок пребывания в днях
              <input
                type="number"
                min={1}
                max={3650}
                value={form.stay_duration_days}
                onChange={(e) =>
                  setForm({ ...form, stay_duration_days: Number(e.target.value) })
                }
              />
            </label>

            <label className="checkbox">
              <input
                type="checkbox"
                checked={form.has_insurance}
                onChange={(e) => setForm({ ...form, has_insurance: e.target.checked })}
              />
              Полис уже есть
            </label>

            <label className="checkbox">
              <input
                type="checkbox"
                checked={form.employment_related}
                onChange={(e) =>
                  setForm({ ...form, employment_related: e.target.checked })
                }
              />
              Случай связан с трудоустройством
            </label>

            <button type="submit" disabled={!canSubmit || loading}>
              {loading ? "Формирование..." : "Сформировать рекомендации"}
            </button>
          </form>

          <div className="hint">
            <strong>Страны для правила полиса:</strong> {countries.join(", ")}
          </div>
          {error && <div className="error">{error}</div>}
        </section>

        <section className="card">
          <h2>Результат</h2>
          {!result && <p className="muted">Заполните форму и отправьте запрос.</p>}

          {result && (
            <>
              <div className="summary">
                <div className="summary-item">
                  <span>Обязательных требований</span>
                  <strong>{result.summary.required_count}</strong>
                </div>
                <div className="summary-item">
                  <span>Необязательных требований</span>
                  <strong>{result.summary.optional_count}</strong>
                </div>
              </div>

              <div className="requirements">
                {result.requirements.map((item) => (
                  <article key={item.code} className="requirement-card">
                    <div className="requirement-top">
                      <h3>{item.title}</h3>
                      <span className={item.required ? "badge badge-danger" : "badge"}>
                        {item.required ? "Требуется" : "Не требуется"}
                      </span>
                    </div>

                    <p><strong>Основание:</strong> {item.reason}</p>
                    {item.deadline && <p><strong>Срок:</strong> {item.deadline}</p>}
                    {item.place && <p><strong>Куда обращаться:</strong> {item.place}</p>}
                  </article>
                ))}
              </div>
            </>
          )}
        </section>

        <section className="card full-width">
          <h2>История запросов</h2>
          {history.length === 0 ? (
            <p className="muted">История пока пуста.</p>
          ) : (
            <div className="history-list">
              {history.map((item) => (
                <article key={item.id} className="history-card">
                  <div className="history-row">
                    <strong>#{item.id}</strong>
                    <span>{new Date(item.created_at).toLocaleString()}</span>
                  </div>
                  <div className="history-row">
                    <span>{item.citizenship}</span>
                    <span>{item.purpose_of_entry}</span>
                    <span>{item.stay_duration_days} дн.</span>
                  </div>
                  <div className="history-row">
                    <span>Мед: {item.medical_required ? "да" : "нет"}</span>
                    <span>Полис: {item.insurance_required ? "да" : "нет"}</span>
                    <span>Полис уже есть: {item.has_insurance ? "да" : "нет"}</span>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
