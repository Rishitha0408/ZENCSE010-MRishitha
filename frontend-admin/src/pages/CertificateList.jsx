import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../api/client'

export default function CertificateList() {
    const [certificates, setCertificates] = useState([])
    const [loading, setLoading] = useState(true)
    const [offset, setOffset] = useState(0)
    const limit = 20
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

    useEffect(() => {
        fetchCertificates()
    }, [offset])

    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-GB') // DD/MM/YYYY
    }

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Issued Certificates</h1>

            {loading ? (
                <div className="flex justify-center p-12">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
            ) : (
                <div className="overflow-x-auto bg-white rounded-lg shadow">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Recipient</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Course</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Issued Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {certificates.map((cert) => (
                                <tr key={cert.certificate_id} className="hover:bg-gray-50 cursor-pointer" onClick={() => navigate(`/certificates/${cert.certificate_id}`)}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{cert.certificate_id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{cert.recipient_name}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{cert.course_title}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatDate(cert.issued_at)}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${cert.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                            {cert.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                        <button
                                            className="text-blue-600 hover:text-blue-900"
                                            onClick={(e) => { e.stopPropagation(); navigate(`/certificates/${cert.certificate_id}`); }}
                                        >
                                            View
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    <div className="px-6 py-4 flex items-center justify-between border-t border-gray-200">
                        <button
                            onClick={() => setOffset(Math.max(0, offset - limit))}
                            disabled={offset === 0}
                            className={`px-4 py-2 border rounded text-sm font-medium ${offset === 0 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                        >
                            Previous
                        </button>
                        <button
                            onClick={() => setOffset(offset + limit)}
                            disabled={certificates.length < limit}
                            className={`ml-3 px-4 py-2 border rounded text-sm font-medium ${certificates.length < limit ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                        >
                            Next
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}
