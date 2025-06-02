'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function LandingPage() {
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      router.push('/emails');
    }, 2000); // Redirect setelah 2 detik

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <main style={styles.container}>
      <div style={styles.loaderWrapper}>
        <img
          src="https://ssl.gstatic.com/ui/v1/icons/mail/rfr/gmail.ico"
          alt="Gmail Logo"
          style={styles.logo}
        />
        <p style={styles.text}>Loading Gmail...</p>
      </div>
      <style jsx>{`
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
        .blinking {
          animation: blink 1s infinite;
        }
      `}</style>
    </main>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    flexDirection: 'column',
  },
  loaderWrapper: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  logo: {
    width: 100,
    height: 100,
    animation: 'blink 1s infinite', // Blink animasi langsung di inline style
  },
  text: {
    marginTop: 20,
    fontSize: 18,
    color: '#555',
    fontFamily: 'Arial, sans-serif',
    animation: 'blink 1s infinite',
  },
};
