import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../api/client'

export default function CertificateList() {
    const [selectedQr, setSelectedQr] = useState(null)
    const [qrModalOpen, setQrModalOpen] = useState(false)
    const [fetchingQr, setFetchingQr] = useState(false)

    const navigate = useNavigate()

    const fetchCertificates = async () => {
        setLoading(true)
        try {
            const data = await apiClient.get(`/api/v1/certificates?skip=${offset}&limit=${limit}`)
            setCertificates(data)
        } catch (error) {
            console.error('Failed to fetch certificates:', error)
        } finally {
            setLoading(false)
        }
    }

    const showQrModal = async (id, e) => {
        e.stopPropagation()
        setFetchingQr(true)
        setQrModalOpen(true)
        try {
            const data = await apiClient.get(`/api/v1/certificates/${id}`)
            setSelectedQr({
                img: data.qr_code_base64,
                id: id,
                name: data.recipient?.name || data.recipient_name
            })
        } catch (error) {
            console.error('Failed to fetch QR:', error)
            setQrModalOpen(false)
        } finally {
            setFetchingQr(false)
        }
    }

    useEffect(() => {
        fetchCertificates()
    }, [offset])

    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-GB') // DD/MM/YYYY
    }

    const filteredCertificates = certificates.filter(cert =>
        cert.recipient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        cert.certificate_id.toLowerCase().includes(searchTerm.toLowerCase())
    )

    return (
        <div className="p-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
                <h1 className="text-2xl font-bold text-gray-900">Issued Certificates</h1>
                <div className="relative w-full md:w-64">
                    <input
                        type="text"
                        placeholder="Search by name or ID..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                    <svg className="w-5 h-5 text-gray-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                </div>
            </div>

            {loading ? (
                <div className="flex justify-center p-12">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
            ) : (
                <div className="overflow-x-auto bg-white rounded-2xl shadow-sm border border-gray-100">
                    <table className="min-w-full divide-y divide-gray-100">
                        <thead className="bg-gray-50/50">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">ID</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Recipient</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Course</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Issued Date</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-4 text-right text-xs font-semibold text-gray-400 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-50">
                            {filteredCertificates.map((cert) => (
                                <tr key={cert.certificate_id} className="hover:bg-blue-50/30 transition-colors group">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">{cert.certificate_id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">{cert.recipient_name}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{cert.course_title}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatDate(cert.issued_at)}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2.5 py-0.5 inline-flex text-[10px] leading-5 font-black uppercase rounded-full ${cert.status === 'ACTIVE' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                            {cert.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-3">
                                        <button
                                            onClick={(e) => showQrModal(cert.certificate_id, e)}
                                            className="text-gray-400 hover:text-blue-600 transition-colors"
                                            title="View QR Code"
                                        >
                                            <svg className="w-5 h-5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
                                            </svg>
                                        </button>
                                        <button
                                            className="text-white bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded-lg text-xs font-bold transition-all shadow-sm"
                                            onClick={() => navigate(`/certificates/${cert.certificate_id}`)}
                                        >
                                            Details
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            {filteredCertificates.length === 0 && (
                                <tr>
                                    <td colSpan="6" className="px-6 py-12 text-center text-gray-400">
                                        No certificates found matching your search.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>

                    <div className="px-6 py-4 flex items-center justify-between border-t border-gray-50 bg-gray-50/30">
                        <button
                            onClick={() => setOffset(Math.max(0, offset - limit))}
                            disabled={offset === 0}
                            className={`px-4 py-2 border border-gray-200 rounded-xl text-xs font-bold transition-all ${offset === 0 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50 hover:shadow-sm'}`}
                        >
                            Previous
                        </button>
                        <span className="text-xs text-gray-400 font-medium">Page {Math.floor(offset / limit) + 1}</span>
                        <button
                            onClick={() => setOffset(offset + limit)}
                            disabled={certificates.length < limit}
                            className={`px-4 py-2 border border-gray-200 rounded-xl text-xs font-bold transition-all ${certificates.length < limit ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50 hover:shadow-sm'}`}
                        >
                            Next
                        </button>
                    </div>
                </div>
            )}

            {/* QR Modal */}
            {qrModalOpen && (
                <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-[2.5rem] shadow-2xl max-w-sm w-full p-8 animate-in fade-in zoom-in duration-300 relative">
                        <button
                            onClick={() => setQrModalOpen(false)}
                            className="absolute top-6 right-6 text-gray-400 hover:text-gray-900 transition-colors"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>

                        <div className="text-center">
                            <h3 className="text-xl font-black text-gray-900 mb-2">Verification QR</h3>
                            <p className="text-gray-500 text-sm mb-8">{selectedQr?.name || 'Loading...'}</p>

                            <div className="bg-gray-50 p-6 rounded-3xl border border-gray-100 flex items-center justify-center mb-6">
                                {fetchingQr ? (
                                    <div className="w-48 h-48 flex items-center justify-center">
                                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                                    </div>
                                ) : (
                                    <img
                                        src={`data:image/png;base64,${selectedQr?.img}`}
                                        alt="QR Code"
                                        className="w-48 h-48 antialiased"
                                    />
                                )}
                            </div>

                            <p className="text-[10px] text-gray-400 font-mono mb-8">{selectedQr?.id}</p>

                            <button
                                onClick={() => setQrModalOpen(false)}
                                className="w-full bg-slate-900 text-white py-4 rounded-2xl font-black hover:bg-black transition-all active:scale-95"
                            >
                                CLOSE
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
