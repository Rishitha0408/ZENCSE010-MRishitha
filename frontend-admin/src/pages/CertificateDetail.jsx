import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import apiClient from '../api/client'

export default function CertificateDetail() {
    const { id } = useParams()
    const navigate = useNavigate()
    const [cert, setCert] = useState(null)
    const [loading, setLoading] = useState(true)
    const [revoking, setRevoking] = useState(false)

    const fetchCertificate = async () => {
        try {
            const data = await apiClient.get(`/api/v1/certificates/${id}`)
            setCert(data)
        } catch (error) {
            console.error('Failed to fetch certificate:', error)
            alert('Certificate not found')
            navigate('/certificates')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchCertificate()
    }, [id])

    const handleRevoke = async () => {
        if (!window.confirm('Are you sure you want to revoke this certificate? This action cannot be undone.')) {
            return
        }

        setRevoking(true)
        try {
            await apiClient.put(`/api/v1/certificates/${id}/revoke`)
            await fetchCertificate() // Refresh data
        } catch (error) {
            console.error('Revocation failed:', error)
            alert('Failed to revoke certificate')
        } finally {
            setRevoking(false)
        }
    }

    const downloadQR = () => {
        const link = document.createElement('a')
        link.href = `data:image/png;base64,${cert.qr_code_base64}`
        link.download = `qr-${id}.png`
        link.click()
    }

    if (loading) return (
        <div className="flex justify-center p-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
    )

    if (!cert) return <div className="p-6">Certificate not found</div>

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <button
                onClick={() => navigate('/certificates')}
                className="mb-6 text-blue-600 hover:underline flex items-center"
            >
                ← Back to List
            </button>

            <div className="bg-white rounded-xl shadow-lg overflow-hidden flex flex-col md:flex-row">
                <div className="p-8 flex-1">
                    <div className="flex justify-between items-start mb-6">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">{cert.certificate?.title || cert.course_title}</h1>
                            <p className="text-gray-500 mt-1">ID: {cert.certificate_id}</p>
                        </div>
                        <span className={`px-4 py-1 rounded-full text-sm font-bold ${cert.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                            {cert.status}
                        </span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                        <section>
                            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Recipient Details</h2>
                            <div className="space-y-2">
                                <p><span className="font-medium">Name:</span> {cert.recipient?.name || cert.recipient_name}</p>
                                <p><span className="font-medium">Email:</span> {cert.recipient?.email || 'N/A'}</p>
                                <p><span className="font-medium">Student ID:</span> {cert.recipient?.student_id || 'N/A'}</p>
                            </div>
                        </section>

                        <section>
                            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Issuance Details</h2>
                            <div className="space-y-2">
                                <p><span className="font-medium">Issued At:</span> {new Date(cert.issued_at).toLocaleString()}</p>
                                <p><span className="font-medium">Expiry:</span> {cert.expiry_date ? new Date(cert.expiry_date).toLocaleDateString() : 'Never'}</p>
                                <p><span className="font-medium">Verifications:</span> {cert.verification_count || 0}</p>
                            </div>
                        </section>
                    </div>

                    <section className="mb-8">
                        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Skills</h2>
                        <div className="flex flex-wrap gap-2">
                            {(cert.certificate?.skills || []).map((skill, i) => (
                                <span key={i} className="bg-blue-50 text-blue-700 px-3 py-1 rounded-md text-sm">
                                    {skill}
                                </span>
                            ))}
                        </div>
                    </section>

                    {cert.status === 'ACTIVE' && (
                        <button
                            onClick={handleRevoke}
                            disabled={revoking}
                            className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
                        >
                            {revoking ? 'Revoking...' : 'Revoke Certificate'}
                        </button>
                    )}
                </div>

                <div className="bg-gray-50 p-8 flex flex-col items-center justify-center border-t md:border-t-0 md:border-l border-gray-100">
                    <div className="bg-white p-4 rounded-lg shadow-sm mb-4">
                        <img
                            src={`data:image/png;base64,${cert.qr_code_base64 || cert.qr?.value}`}
                            alt="QR Code"
                            className="w-48 h-48"
                        />
                    </div>
                    <button
                        onClick={downloadQR}
                        className="text-gray-600 hover:text-gray-900 flex items-center font-medium"
                    >
                        Download QR Code
                    </button>
                </div>
            </div>
        </div>
    )
}
