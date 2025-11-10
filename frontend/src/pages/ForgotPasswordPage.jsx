import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import authService from '../services/authService';

/**
 * Página para solicitar recuperación de contraseña
 */
function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await authService.requestPasswordReset(email);
      setEmailSent(true);
      toast.success('Email enviado! Revisa tu bandeja de entrada', {
        duration: 5000,
      });
    } catch (error) {
      console.error('Error al solicitar recuperación:', error);

      // Manejar rate limiting (429)
      if (error.response?.status === 429) {
        toast.error(
          'Demasiados intentos. Por favor espera una hora antes de intentar nuevamente.',
          { duration: 6000 }
        );
      } else {
        // Mostrar mensaje genérico por seguridad (prevenir email enumeration)
        toast.error('Hubo un error. Intenta nuevamente más tarde.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (emailSent) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <div style={styles.successIcon}>📧</div>
          <h1 style={styles.title}>Email Enviado</h1>
          <p style={styles.description}>
            Si el email <strong>{email}</strong> está registrado en nuestro sistema,
            recibirás un correo con instrucciones para restablecer tu contraseña.
          </p>
          <div style={styles.infoBox}>
            <p style={{ margin: 0 }}>
              <strong>⚠️ Importante:</strong>
            </p>
            <ul style={{ marginTop: '10px', marginBottom: 0, paddingLeft: '20px' }}>
              <li>Revisa tu carpeta de SPAM</li>
              <li>El link expira en 30 minutos</li>
              <li>Solo puedes usar el link una vez</li>
            </ul>
          </div>
          <Link to="/login" style={styles.backButton}>
            Volver al inicio de sesión
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>¿Olvidaste tu contraseña?</h1>
        <p style={styles.subtitle}>
          Ingresa tu email y te enviaremos instrucciones para restablecer tu contraseña
        </p>

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={styles.input}
              placeholder="tu@email.com"
              autoFocus
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            style={{
              ...styles.button,
              ...(isLoading ? styles.buttonDisabled : {})
            }}
          >
            {isLoading ? 'Enviando...' : 'Enviar instrucciones'}
          </button>
        </form>

        <p style={styles.footer}>
          ¿Recordaste tu contraseña?{' '}
          <Link to="/login" style={styles.link}>
            Inicia sesión
          </Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '20px'
  },
  card: {
    backgroundColor: 'white',
    padding: '40px',
    borderRadius: '8px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    width: '100%',
    maxWidth: '450px'
  },
  title: {
    margin: '0 0 10px 0',
    fontSize: '24px',
    fontWeight: 'bold',
    textAlign: 'center'
  },
  subtitle: {
    margin: '0 0 30px 0',
    color: '#666',
    textAlign: 'center',
    fontSize: '14px',
    lineHeight: '1.5'
  },
  description: {
    margin: '20px 0',
    color: '#333',
    textAlign: 'center',
    fontSize: '14px',
    lineHeight: '1.6'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px'
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '5px'
  },
  label: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#333'
  },
  input: {
    padding: '10px',
    fontSize: '14px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    outline: 'none',
    transition: 'border-color 0.3s'
  },
  button: {
    padding: '12px',
    fontSize: '16px',
    fontWeight: '500',
    color: 'white',
    backgroundColor: '#007bff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    transition: 'background-color 0.3s'
  },
  buttonDisabled: {
    backgroundColor: '#6c757d',
    cursor: 'not-allowed'
  },
  footer: {
    marginTop: '20px',
    textAlign: 'center',
    fontSize: '14px',
    color: '#666'
  },
  link: {
    color: '#007bff',
    textDecoration: 'none',
    fontWeight: '500'
  },
  successIcon: {
    fontSize: '64px',
    textAlign: 'center',
    marginBottom: '20px'
  },
  infoBox: {
    backgroundColor: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '4px',
    padding: '15px',
    margin: '20px 0',
    fontSize: '13px',
    color: '#856404'
  },
  backButton: {
    display: 'block',
    textAlign: 'center',
    padding: '12px',
    marginTop: '20px',
    fontSize: '16px',
    fontWeight: '500',
    color: '#007bff',
    textDecoration: 'none',
    border: '1px solid #007bff',
    borderRadius: '4px',
    transition: 'all 0.3s'
  }
};

export default ForgotPasswordPage;
