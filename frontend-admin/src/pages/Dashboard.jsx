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
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    const fetchStats = async (isRefresh = false) => {
        if (!isRefresh) setLoading(true)
        setError(null)
        try {
            const data = await apiClient.get('/api/v1/stats/')
            setStats(data)
        } catch (err) {
            console.error('Failed to fetch stats:', err)
            setError('Could not load statistics.')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchStats()
        const interval = setInterval(() => fetchStats(true), 30000)
        return () => clearInterval(interval)
    }, [])

    if (error) return (
        <div className="p-6 text-red-600 bg-red-50 rounded-lg m-6 border border-red-200">
            {error} <button onClick={() => fetchStats()} className="underline ml-2">Retry</button>
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

            <div className="mt-12 bg-blue-50 p-8 rounded-2xl border border-blue-100 flex items-center justify-between">
                <div>
                    <h2 className="text-xl font-bold text-blue-900">Certificate Generation</h2>
                    <p className="text-blue-700 mt-1">Issue new tamper-proof certificates via the API or CLI.</p>
                </div>
                <button
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-blue-700 transition-colors"
                    onClick={() => navigate('/issue')}
                >
                    Issue Certificate
                </button>
            </div>
        </div>
    )
}
