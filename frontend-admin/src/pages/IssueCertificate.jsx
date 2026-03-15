import React, { useState } from 'react'
import apiClient from '../api/client'

export default function IssueCertificate() {
    const [formData, setFormData] = useState({
        recipient_name: '',
        recipient_email: '',
        recipient_student_id: '',
        course_title: '',
        description: '',
        skills: [],
        issue_date: new Date().toISOString().split('T')[0],
        expiry_date: ''
    })

    const [skillInput, setSkillInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [successData, setSuccessData] = useState(null)
    const [errors, setErrors] = useState({})
    const [generalError, setGeneralError] = useState('')

    const handleInputChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({ ...prev, [name]: value }))
        // Clear error for this field
        if (errors[name]) {
            setErrors(prev => {
                const newErrors = { ...prev }
                delete newErrors[name]
                return newErrors
            })
        }
    }

    const addSkill = (e) => {
        e.preventDefault()
        if (skillInput.trim() && !formData.skills.includes(skillInput.trim())) {
            setFormData(prev => ({
                ...prev,
                skills: [...prev.skills, skillInput.trim()]
            }))
            setSkillInput('')
        }
    }

    const removeSkill = (skillToRemove) => {
        setFormData(prev => ({
            ...prev,
            skills: prev.skills.filter(s => s !== skillToRemove)
        }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setErrors({})
        setGeneralError('')
        setSuccessData(null)

        try {
            const payload = {
                ...formData,
                expiry_date: formData.expiry_date || null
            }
            const response = await apiClient.post('/api/v1/certificates/', payload)
            setSuccessData(response)
        } catch (err) {
            if (err.details) {
                // Map Pydantic errors to field names
                const fieldErrors = {}
                err.details.forEach(detail => {
                    const field = detail.loc[detail.loc.length - 1]
                    fieldErrors[field] = detail.msg
                })
                setErrors(fieldErrors)
            } else {
                setGeneralError(err.message || 'Failed to issue certificate')
            }
        } finally {
            setLoading(false)
        }
    }

    const downloadQR = () => {
        const link = document.createElement('a')
        link.href = `data:image/png;base64,${successData.qr_code_base64}`
        link.download = `certificate-${successData.certificate_id}.png`
        link.click()
    }

    if (successData) {
        return (
            <div className="p-8 max-w-2xl mx-auto">
                <div className="bg-white rounded-2xl shadow-xl p-8 text-center border border-green-100">
                    <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                        </svg>
                    </div>
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">Certificate Issued!</h2>
                    <p className="text-gray-500 mb-8">Certificate ID: <span className="font-mono font-bold text-blue-600">{successData.certificate_id}</span></p>

                    <div className="bg-gray-50 p-6 rounded-xl inline-block mb-8">
                        <img
                            src={`data:image/png;base64,${successData.qr_code_base64}`}
                            alt="QR Code"
                            className="w-48 h-48 mx-auto shadow-sm bg-white p-2 rounded-lg"
                        />
                    </div>

                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <button
                            onClick={downloadQR}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-bold transition-all shadow-lg hover:shadow-blue-200"
                        >
                            Download QR Code
                        </button>
                        <button
                            onClick={() => {
                                setSuccessData(null)
                                setFormData({
                                    recipient_name: '',
                                    recipient_email: '',
                                    recipient_student_id: '',
                                    course_title: '',
                                    description: '',
                                    skills: [],
                                    issue_date: new Date().toISOString().split('T')[0],
                                    expiry_date: ''
                                })
                            }}
                            className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-8 py-3 rounded-xl font-bold transition-all"
                        >
                            Issue Another
                        </button>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="p-8 max-w-4xl mx-auto">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Issue New Certificate</h1>
                <p className="text-gray-500 mt-2">Create a tamper-proof digital credential for a student.</p>
            </div>

            {generalError && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-600 rounded-xl flex items-center gap-3">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    {generalError}
                </div>
            )}

            <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Recipient Info */}
                    <div className="space-y-6">
                        <h2 className="text-sm font-bold text-gray-400 uppercase tracking-widest border-b pb-2">Recipient</h2>

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name *</label>
                            <input
                                type="text"
                                name="recipient_name"
                                required
                                value={formData.recipient_name}
                                onChange={handleInputChange}
                                className={`w-full px-4 py-3 rounded-xl border ${errors.recipient_name ? 'border-red-500' : 'border-gray-200'} focus:ring-2 focus:ring-blue-500 outline-none transition-all`}
                                placeholder="e.g. John Doe"
                            />
                            {errors.recipient_name && <p className="mt-1 text-xs text-red-500">{errors.recipient_name}</p>}
                        </div>

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">Email Address *</label>
                            <input
                                type="email"
                                name="recipient_email"
                                required
                                value={formData.recipient_email}
                                onChange={handleInputChange}
                                className={`w-full px-4 py-3 rounded-xl border ${errors.recipient_email ? 'border-red-500' : 'border-gray-200'} focus:ring-2 focus:ring-blue-500 outline-none transition-all`}
                                placeholder="john@example.com"
                            />
                            {errors.recipient_email && <p className="mt-1 text-xs text-red-500">{errors.recipient_email}</p>}
                        </div>

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">Student ID (Optional)</label>
                            <input
                                type="text"
                                name="recipient_student_id"
                                value={formData.recipient_student_id}
                                onChange={handleInputChange}
                                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                                placeholder="e.g. STU-2024-001"
                            />
                        </div>
                    </div>

                    {/* Certificate Info */}
                    <div className="space-y-6">
                        <h2 className="text-sm font-bold text-gray-400 uppercase tracking-widest border-b pb-2">Certificate</h2>

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">Course Title *</label>
                            <input
                                type="text"
                                name="course_title"
                                required
                                value={formData.course_title}
                                onChange={handleInputChange}
                                className={`w-full px-4 py-3 rounded-xl border ${errors.course_title ? 'border-red-500' : 'border-gray-200'} focus:ring-2 focus:ring-blue-500 outline-none transition-all`}
                                placeholder="e.g. Full Stack Web Development"
                            />
                            {errors.course_title && <p className="mt-1 text-xs text-red-500">{errors.course_title}</p>}
                        </div>

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 mb-2">Description (Optional)</label>
                            <textarea
                                name="description"
                                rows="3"
                                value={formData.description}
                                onChange={handleInputChange}
                                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-none"
                                placeholder="Briefly describe the achievement..."
                            ></textarea>
                        </div>
                    </div>
                </div>

                {/* Dynamic Skills */}
                <div className="mt-8">
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Skills (Add tags)</label>
                    <div className="flex gap-2 mb-3">
                        <input
                            type="text"
                            value={skillInput}
                            onChange={(e) => setSkillInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && addSkill(e)}
                            className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                            placeholder="e.g. React"
                        />
                        <button
                            onClick={addSkill}
                            type="button"
                            className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-2 rounded-xl font-bold transition-all"
                        >
                            Add
                        </button>
                    </div>
                    <div className="flex flex-wrap gap-2">
                        {formData.skills.map(skill => (
                            <span key={skill} className="bg-blue-50 text-blue-700 px-3 py-1.5 rounded-lg text-sm font-medium flex items-center gap-2 group">
                                {skill}
                                <button
                                    onClick={() => removeSkill(skill)}
                                    className="text-blue-300 hover:text-blue-600 transition-colors"
                                >
                                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                    </svg>
                                </button>
                            </span>
                        ))}
                    </div>
                </div>

                {/* Dates */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">Issue Date *</label>
                        <input
                            type="date"
                            name="issue_date"
                            required
                            value={formData.issue_date}
                            onChange={handleInputChange}
                            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">Expiry Date (Optional)</label>
                        <input
                            type="date"
                            name="expiry_date"
                            value={formData.expiry_date}
                            onChange={handleInputChange}
                            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                        />
                    </div>
                </div>

                <div className="mt-12 flex justify-end">
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full md:w-auto bg-blue-600 hover:bg-blue-700 text-white px-12 py-4 rounded-2xl font-bold transition-all shadow-lg hover:shadow-blue-200 disabled:opacity-50"
                    >
                        {loading ? 'Issuing...' : 'Issue Certificate'}
                    </button>
                </div>
            </form>
        </div>
    )
}
