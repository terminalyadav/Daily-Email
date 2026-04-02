import { useState, useEffect, useCallback } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function StatCard({ icon, label, value, sub, color }) {
  return (
    <div className={`stat-card ${color}`}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-info">
        <div className="stat-value">{value ?? '—'}</div>
        <div className="stat-label">{label}</div>
        {sub && <div className="stat-sub">{sub}</div>}
      </div>
    </div>
  )
}

function Pill({ children, active, onClick }) {
  return (
    <button className={`pill ${active ? 'active' : ''}`} onClick={onClick}>
      {children}
    </button>
  )
}

function formatDate(d) {
  if (!d) return ''
  const [y, m, day] = d.split('-')
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  return `${parseInt(day)} ${months[parseInt(m)-1]} ${y}`
}

export default function App() {
  const [dates, setDates]           = useState([])
  const [stats, setStats]           = useState(null)
  const [selectedDate, setSelected] = useState(null)
  const [dayData, setDayData]       = useState(null)
  const [loading, setLoading]       = useState(false)
  const [search, setSearch]         = useState('')
  const [platform, setPlatform]     = useState('All')
  const [sortCol, setSortCol]       = useState('username')
  const [sortAsc, setSortAsc]       = useState(true)
  const [error, setError]           = useState(null)
  const [isTriggering, setIsTriggering] = useState(false)
  const [triggerMsg, setTriggerMsg] = useState(null)

  // Load dates list + stats on mount
  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE}/api/dates`).then(r => r.json()),
      fetch(`${API_BASE}/api/stats`).then(r => r.json()),
    ]).then(([d, s]) => {
      setDates(d.dates || [])
      setStats(s)
      if (d.dates?.length) setSelected(d.dates[0].date)
    }).catch(() => setError('Backend se connect nahi ho pa raha. Backend run hai?'))
  }, [])

  // Load day data when date changes
  useEffect(() => {
    if (!selectedDate) return
    setLoading(true)
    setDayData(null)
    fetch(`${API_BASE}/api/emails/${selectedDate}`)
      .then(r => r.json())
      .then(d => { setDayData(d); setLoading(false) })
      .catch(() => { setError('Data load nahi hua.'); setLoading(false) })
  }, [selectedDate])

  const handleDownload = useCallback(async () => {
    if (!selectedDate) return
    const res = await fetch(`${API_BASE}/api/download/${selectedDate}`)
    const blob = await res.blob()
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href     = url
    a.download = `${selectedDate} emails.xlsx`
    a.click()
    URL.revokeObjectURL(url)
  }, [selectedDate])

  const handleTrigger = useCallback(async () => {
    setIsTriggering(true)
    setTriggerMsg(null)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/api/trigger`, { method: 'POST' })
      if (!res.ok) {
        const data = await res.json()
        setError(data.detail || 'Failed to trigger background job.')
      } else {
        setTriggerMsg('Background job started! Dashboard will update in ~30s. Please refresh manually or wait.')
      }
    } catch (e) {
      setError('Network error: Is backend running?')
    } finally {
      setIsTriggering(false)
    }
  }, [])

  const toggleSort = (col) => {
    if (sortCol === col) setSortAsc(a => !a)
    else { setSortCol(col); setSortAsc(true) }
  }

  const records = dayData?.records || []
  const filtered = records
    .filter(r => platform === 'All' || r.platform === platform)
    .filter(r => {
      if (!search) return true
      const s = search.toLowerCase()
      return r.email.toLowerCase().includes(s) || r.username.toLowerCase().includes(s)
    })
    .sort((a, b) => {
      const v = sortAsc ? 1 : -1
      return a[sortCol]?.localeCompare(b[sortCol]) * v
    })

  const tikCount = records.filter(r => r.platform === 'TikTok').length
  const igCount  = records.filter(r => r.platform === 'Instagram').length

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="logo">📩</div>
          <div>
            <h1>Daily Email Dashboard</h1>
            <p className="sub">Influencer outreach — fresh leads per day</p>
          </div>
        </div>
        <div className="header-right" style={{ display: 'flex', gap: '10px' }}>
          <button className={`btn-trigger ${isTriggering ? 'loading' : ''}`} onClick={handleTrigger} disabled={isTriggering}>
            {isTriggering ? '⏳ Processing...' : '🔄 Fetch Latest Data'}
          </button>
          {selectedDate && (
            <button className="btn-download" onClick={handleDownload}>
              ⬇ Download .xlsx
            </button>
          )}
        </div>
      </header>

      {error && <div className="error-banner">⚠️ {error}</div>}
      {triggerMsg && <div className="success-banner">✨ {triggerMsg}</div>}

      {/* Overall stats */}
      {stats && (
        <div className="stats-row">
          <StatCard icon="📋" label="Total Records (All Time)" value={stats.total_records?.toLocaleString()} color="blue" />
          <StatCard icon="🎵" label="TikTok (All Time)"        value={stats.tiktok_total?.toLocaleString()}  color="pink" />
          <StatCard icon="📷" label="Instagram (All Time)"     value={stats.instagram_total?.toLocaleString()} color="purple" />
          <StatCard icon="📅" label="Days Recorded"            value={stats.days_recorded}                   color="green" />
        </div>
      )}

      <div className="main-layout">
        {/* Sidebar: date list */}
        <aside className="sidebar">
          <h2 className="sidebar-title">📆 Select Date</h2>
          <div className="date-list">
            {dates.map(d => (
              <div
                key={d.date}
                className={`date-item ${selectedDate === d.date ? 'active' : ''}`}
                onClick={() => setSelected(d.date)}
              >
                <div className="date-item-label">{formatDate(d.date)}</div>
                <div className="date-item-count">
                  <span className="badge total">{d.total}</span>
                  {d.tiktok_count > 0    && <span className="badge tiktok">TT {d.tiktok_count}</span>}
                  {d.instagram_count > 0 && <span className="badge ig">IG {d.instagram_count}</span>}
                </div>
              </div>
            ))}
            {dates.length === 0 && <p className="no-data">No dates yet.<br/>Run migration script.</p>}
          </div>
        </aside>

        {/* Main content */}
        <main className="content">
          {selectedDate && (
            <>
              <div className="content-header">
                <div>
                  <h2>{formatDate(selectedDate)}</h2>
                  {dayData && (
                    <p className="day-sub">
                      {dayData.total} fresh records — {tikCount} TikTok · {igCount} Instagram
                    </p>
                  )}
                </div>
                <div className="content-controls">
                  <div className="platform-pills">
                    {['All','TikTok','Instagram'].map(p => (
                      <Pill key={p} active={platform===p} onClick={() => setPlatform(p)}>{p}</Pill>
                    ))}
                  </div>
                  <input
                    className="search-box"
                    placeholder="🔍 Search email or username..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                  />
                </div>
              </div>

              {loading ? (
                <div className="loading">
                  <div className="spinner" />
                  <p>Loading records...</p>
                </div>
              ) : (
                <>
                  <div className="table-wrap">
                    <table className="email-table">
                      <thead>
                        <tr>
                          {['platform','username','email'].map(col => (
                            <th key={col} onClick={() => toggleSort(col)} className="sortable">
                              {col.charAt(0).toUpperCase() + col.slice(1)}
                              {sortCol === col && (
                                <span className="sort-arrow">{sortAsc ? ' ↑' : ' ↓'}</span>
                              )}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {filtered.map((r, i) => (
                          <tr key={i} className={i % 2 === 0 ? 'even' : 'odd'}>
                            <td>
                              <span className={`platform-tag ${r.platform === 'TikTok' ? 'tiktok' : 'ig'}`}>
                                {r.platform === 'TikTok' ? '🎵' : '📷'} {r.platform}
                              </span>
                            </td>
                            <td className="username-cell">{r.username}</td>
                            <td>
                              <a href={`mailto:${r.email}`} className="email-link">{r.email}</a>
                            </td>
                          </tr>
                        ))}
                        {filtered.length === 0 && (
                          <tr><td colSpan={3} className="no-results">No records match your filters.</td></tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                  <div className="table-footer">
                    Showing <strong>{filtered.length}</strong> of <strong>{records.length}</strong> records
                  </div>
                </>
              )}
            </>
          )}
          {!selectedDate && !loading && (
            <div className="empty-state">
              <div className="empty-icon">📅</div>
              <p>Left side se koi date select karo</p>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
