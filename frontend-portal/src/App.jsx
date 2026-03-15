import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const VerificationPortal = () => {
    const [certId, setCertId] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Extract ID from URL if present (e.g., /verify/CERT-123 or /v/CERT-123)
    useEffect(() => {
        const path = window.location.pathname;
        const match = path.match(/\/(?:verify|v)\/(CERT-[\w-]+)/);
        if (match && match[1]) {
            verifyCertificate(match[1]);
        }
    }, []);

    const verifyCertificate = async (id) => {
        const targetId = id || certId;
        if (!targetId) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await axios.get(`${API_URL}/api/v1/verify/${targetId}`);
            setResult(response.data);
            if (!id && certId) setCertId(''); // Clear input on manual search success
        } catch (err) {
            setError(err.response?.data?.error || 'Verification failed. Please check the ID and try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12 md:py-24">
            <div className="text-center mb-16">
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-full text-sm font-bold mb-6">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 4.946-2.597 9.29-6.518 11.771a1.304 1.304 0 01-1.482 0C6.097 16.29 3.5 11.946 3.5 7c0-.68.056-1.35.166-2.001zm6.34 1.557a1 1 0 011.415 0l3.917 3.917a1 1 0 11-1.414 1.414L10 9.414l-2.424 2.424a1 1 0 11-1.414-1.414l2.917-2.917-.073-.073z" clipRule="evenodd" />
                    </svg>
                    TAMPER-PROOF VERIFICATION
                </div>
                <h1 className="text-5xl md:text-6xl font-black text-slate-900 tracking-tight mb-6">
                    Verify <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Credential</span>
                </h1>
                <p className="text-lg text-slate-500 max-w-xl mx-auto">
                    Instantly validate the authenticity of any CertShield digital certificate using its unique identifier.
                </p>
            </div>

            <div className="max-w-2xl mx-auto mb-12">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
                    <div className="bg-blue-600 p-8 rounded-3xl text-white shadow-xl shadow-blue-200">
                        <div className="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center mb-4">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
                            </svg>
                        </div>
                        <h3 className="text-xl font-bold mb-2">Scan QR Code</h3>
                        <p className="text-blue-100 text-sm">Point your camera at the certificate QR code for instant results.</p>
                    </div>
                    <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-xl shadow-slate-100">
                        <div className="w-12 h-12 bg-slate-100 rounded-2xl flex items-center justify-center mb-4 text-slate-600">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </div>
                        <h3 className="text-xl font-bold mb-2 text-slate-900">Manual Search</h3>
                        <p className="text-slate-500 text-sm">Enter the unique Certificate ID below to verify the credential.</p>
                    </div>
                </div>

                <div className="relative group">
                    <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-[2rem] blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                    <div className="relative bg-white p-2 rounded-[1.8rem] shadow-2xl border border-slate-100">
                        <div className="flex flex-col md:flex-row gap-2">
                            <div className="flex-1 relative">
                                <input
                                    type="text"
                                    placeholder="Enter Certificate ID..."
                                    className="w-full px-8 py-5 rounded-2xl bg-slate-50 border-none focus:ring-0 outline-none text-lg font-medium tracking-wide"
                                    value={certId}
                                    onChange={(e) => setCertId(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && verifyCertificate()}
                                />
                                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-300 font-mono text-xs hidden md:block">
                                    PRESS ENTER ↵
                                </div>
                            </div>
                            <button
                                onClick={() => verifyCertificate()}
                                disabled={loading}
                                className="bg-slate-900 hover:bg-black text-white px-10 py-5 rounded-2xl font-bold transition-all shadow-xl hover:shadow-slate-200 active:scale-95 disabled:opacity-50"
                            >
                                {loading ? 'VERIFYING...' : 'VERIFY NOW'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {error && (
                <div className="bg-red-50 border border-red-100 text-red-600 p-6 rounded-2xl flex items-center gap-4 max-w-2xl mx-auto animate-shake">
                    <svg className="w-6 h-6 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    <span className="font-medium text-lg">{error}</span>
                </div>
            )}

            {result && (
                <div className="max-w-2xl mx-auto animate-fade-in-up">
                    <div className={`p-8 rounded-3xl border shadow-xl ${result.result === 'VALID' ? 'bg-emerald-50 border-emerald-100' : 'bg-amber-50 border-amber-100'}`}>
                        <div className="flex justify-between items-start mb-8">
                            <div>
                                <h2 className="text-3xl font-black text-slate-900 mb-1">{result.course_title}</h2>
                                <p className="text-slate-500 font-medium tracking-wide">STUDENT: {result.recipient_name}</p>
                            </div>
                            <div className={`px-4 py-2 rounded-full text-xs font-black uppercase tracking-widest ${result.result === 'VALID' ? 'bg-emerald-500 text-white' : 'bg-amber-500 text-white'}`}>
                                {result.result}
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-6 pt-6 border-t border-slate-200/50">
                            <div>
                                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Institution</p>
                                <p className="font-bold text-slate-800">{result.institution_name}</p>
                            </div>
                            <div>
                                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Issue Date</p>
                                <p className="font-bold text-slate-800">{new Date(result.issued_at).toLocaleDateString()}</p>
                            </div>
                        </div>

                        {result.result === 'VALID' && result.linkedin_share_url && (
                            <div className="mt-8">
                                <a
                                    href={result.linkedin_share_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="inline-flex items-center gap-2 bg-[#0a66c2] hover:bg-[#004182] text-white px-6 py-3 rounded-xl font-bold transition-all shadow-lg active:scale-95"
                                >
                                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
                                    </svg>
                                    Add to LinkedIn
                                </a>
                            </div>
                        )}

                        <div className="mt-8 p-4 bg-white/50 rounded-xl border border-white/50 text-sm text-slate-600 italic">
                            "{result.message}"
                        </div>

                        <button
                            onClick={() => setResult(null)}
                            className="w-full mt-6 py-4 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-bold transition-all border border-slate-200"
                        >
                            VERIFY ANOTHER CERTIFICATE
                        </button>
                    </div>
                </div>
            )}

            <div className="mt-24 text-center">
                <p className="text-slate-400 text-sm font-medium tracking-widest uppercase mb-4">Powered by</p>
                <div className="flex items-center justify-center gap-3 grayscale opacity-30">
                    <div className="w-8 h-8 bg-slate-900 rounded-lg"></div>
                    <span className="text-xl font-black text-slate-900">CERTSHIELD</span>
                </div>
            </div>

            <style>{`
        @keyframes fade-in-up {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
        .animate-fade-in-up { animation: fade-in-up 0.5s ease-out forwards; }
        .animate-shake { animation: shake 0.2s ease-in-out infinite; animation-iteration-count: 2; }
      `}</style>
        </div>
    );
};

export default VerificationPortal;
