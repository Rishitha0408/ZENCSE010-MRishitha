import React from 'react'
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import CertificateList from './pages/CertificateList'
import CertificateDetail from './pages/CertificateDetail'
import IssueCertificate from './pages/IssueCertificate'

const NavLink = ({ to, children }) => {
    const location = useLocation()
    const isActive = location.pathname === to
    return (
        <Link
            to={to}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${isActive ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
        >
            {children}
        </Link>
    )
}

function App() {
    return (
        <BrowserRouter>
            <div className="min-h-screen bg-gray-50 flex">
                {/* Sidebar */}
                <div className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col">
                    <div className="flex items-center gap-3 mb-10">
                        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold">C</span>
                        </div>
                        <span className="text-xl font-bold text-gray-900 tracking-tight">CertShield</span>
                    </div>

                    <nav className="flex flex-col gap-2 flex-grow">
                        <NavLink to="/">Dashboard</NavLink>
                        <NavLink to="/certificates">Certificates</NavLink>
                        <NavLink to="/issue">Issue</NavLink>
                    </nav>

                    <div className="mt-auto pt-6 border-t border-gray-100 text-xs text-gray-400">
                        Admin Panel v1.0.0
                    </div>
                </div>

                {/* Main Content */}
                <div className="flex-1 overflow-auto">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/certificates" element={<CertificateList />} />
                        <Route path="/certificates/:id" element={<CertificateDetail />} />
                        <Route path="/issue" element={<IssueCertificate />} />
                    </Routes>
                </div>
            </div>
        </BrowserRouter>
    )
}

export default App
