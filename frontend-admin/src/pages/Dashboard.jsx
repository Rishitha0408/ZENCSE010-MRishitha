import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../api/client'

const StatCard = ({ title, value, color, loading }) => (
    <div className="bg-white p-6 rounded-xl shadow-md border-l-4" style={{ borderColor: color }}>
        <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider">{title}</h3>
        {loading ? (
            <div className="h-8 w-24 bg-gray-100 animate-pulse mt-2 rounded"></div>
        ) : (
            <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        )}
    </div>
)

export default function Dashboard() {
    const navigate = useNavigate()
    const [stats, setStats] = useState(null)
    const [recentCerts, setRecentCerts] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    const fetchData = async (isRefresh = false) => {
        if (!isRefresh) setLoading(true)
        setError(null)
        try {
            const [statsRes, certsRes] = await Promise.all([
                apiClient.get('/api/v1/stats/'),
                apiClient.get('/api/v1/certificates/?limit=5')
            ])
            setStats(statsRes)
            setRecentCerts(certsRes)
        } catch (err) {
            console.error('Failed to fetch dashboard data:', err)
            setError('Could not load statistics.')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchData()
        const interval = setInterval(() => fetchData(true), 30000)
        return () => clearInterval(interval)
    }, [])

    if (error) return (
        <div className="p-6 text-red-600 bg-red-50 rounded-lg m-6 border border-red-200">
            {error} <button onClick={() => fetchData()} className="underline ml-2">Retry</button>
        </div>
    )

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
                <span className="text-xs text-gray-400">Updates every 30 seconds</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Total Issued"
                    value={stats?.total}
                    color="#3b82f6"
                    loading={loading}
                />
                <StatCard
                    title="Active"
                    value={stats?.active}
                    color="#10b981"
                    loading={loading}
                />
                <StatCard
                    title="Revoked"
                    value={stats?.revoked}
                    color="#ef4444"
                    loading={loading}
                />
                <StatCard
                    title="Verifications Today"
                    value={stats?.verifications_today}
                    color="#f59e0b"
                    loading={loading}
                />
            </div>

            <div className="mt-12 grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                    <div className="p-6 border-b border-gray-50 flex justify-between items-center">
                        <h2 className="font-bold text-gray-900">Recent Certificates</h2>
                        <button onClick={() => navigate('/certificates')} className="text-blue-600 text-sm hover:underline">View All</button>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead className="bg-gray-50 text-gray-400 uppercase text-xs font-semibold">
                                <tr>
                                    <th className="px-6 py-4">Recipient</th>
                                    <th className="px-6 py-4">Title</th>
                                    <th className="px-6 py-4">Status</th>
                                    <th className="px-6 py-4 text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-50">
                                {recentCerts.map((cert) => (
                                    <tr key={cert.certificate_id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4 font-medium text-gray-900">{cert.recipient_name}</td>
                                        <td className="px-6 py-4 text-gray-500">{cert.course_title}</td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded-full text-[10px] font-bold ${cert.status === 'ACTIVE' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                                {cert.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <button
                                                onClick={() => navigate(`/certificates/${cert.certificate_id}`)}
                                                className="text-blue-600 hover:text-blue-800 font-medium text-sm"
                                            >
                                                Details
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                                {recentCerts.length === 0 && !loading && (
                                    <tr>
                                        <td colSpan="4" className="px-6 py-8 text-center text-gray-400">No certificates issued yet.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="bg-blue-600 rounded-2xl p-8 text-white flex flex-col justify-between shadow-xl shadow-blue-100">
                    <div>
                        <h2 className="text-2xl font-bold mb-4">Quick Issue</h2>
                        <p className="text-blue-100 mb-8">Generate a new tamper-proof digital certificate in seconds.</p>
                        <ul className="space-y-3 text-sm text-blue-50">
                            <li className="flex items-center gap-2">
                                <span className="w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center text-[10px]">✓</span>
                                Cryptographic Security
                            </li>
                            <li className="flex items-center gap-2">
                                <span className="w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center text-[10px]">✓</span>
                                Instant QR Validation
                            </li>
                            <li className="flex items-center gap-2">
                                <span className="w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center text-[10px]">✓</span>
                                LinkedIn Integration
                            </li>
                        </ul>
                    </div>
                    <button
                        className="bg-white text-blue-600 w-full py-4 rounded-xl font-bold hover:bg-blue-50 transition-colors shadow-lg"
                        onClick={() => navigate('/issue')}
                    >
                        Create Certificate
                    </button>
                </div>
            </div>
        </div>
    )
}
