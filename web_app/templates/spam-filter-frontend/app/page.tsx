'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function LandingPage() {
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      router.push('/emails');
    }, 2000); // tunggu 2 detik sebelum redirect

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <main style={styles.container}>
      <img
        src="https://ssl.gstatic.com/ui/v1/icons/mail/rfr/gmail.ico"
        alt="Gmail Logo"
        style={styles.logo}
      />
    </main>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  logo: {
    width: 150,
    animation: 'blink 1s infinite',
  },
};

// Animasi CSS global untuk blink
// Jika pakai file CSS global, masukkan @keyframes di situ,
// tapi di sini kita inject dengan <style> di Head:

import React from 'react';

export function Head() {
  return (
    <style>{`
      @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
      }
      img {
        animation: blink 1s infinite;
      }
    `}</style>
  );
}
