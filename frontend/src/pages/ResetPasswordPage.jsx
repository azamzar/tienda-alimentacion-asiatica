import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import authService from '../services/authService';

/**
 * Página para restablecer contraseña con token
 */
function ResetPasswordPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');

  const [formData, setFormData] = useState({
    newPassword: '',
    confirmPassword: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [passwordResetSuccess, setPasswordResetSuccess] = useState(false);

  // Verificar que hay un token
  useEffect(() => {
    if (!token) {
      toast.error('Token inválido o faltante');
      navigate('/forgot-password');
    }
  }, [token, navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validar que las contraseñas coincidan
    if (formData.newPassword !== formData.confirmPassword) {
      toast.error('Las contraseñas no coinciden');
      return;
    }

    // Validar longitud mínima
    if (formData.newPassword.length < 6) {
      toast.error('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    setIsLoading(true);

    try {
      await authService.confirmPasswordReset({
        token,
        new_password: formData.newPassword
      });

      setPasswordResetSuccess(true);
      toast.success('¡Contraseña restablecida exitosamente!');

      // Redirigir al login después de 3 segundos
      setTimeout(() => {
        navigate('/login');
      }, 3000);
    } catch (error) {
      console.error('Error al restablecer contraseña:', error);

      if (error.response?.status === 400) {
        toast.error('El token es inválido o ha expirado. Solicita uno nuevo.');
      } else {
        toast.error('Error al restablecer contraseña. Intenta nuevamente.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (passwordResetSuccess) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <div style={styles.successIcon}>✓</div>
          <h1 style={styles.title}>¡Contraseña Restablecida!</h1>
          <p style={styles.description}>
            Tu contraseña ha sido cambiada exitosamente.
          </p>
          <p style={styles.description}>
            Redirigiendo al inicio de sesión en 3 segundos...
          </p>
          <Link to="/login" style={styles.button}>
            Ir al inicio de sesión ahora
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Restablecer Contraseña</h1>
        <p style={styles.subtitle}>
          Ingresa tu nueva contraseña
        </p>

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Nueva Contraseña</label>
            <input
              type="password"
              name="newPassword"
              value={formData.newPassword}
              onChange={handleChange}
              required
              minLength={6}
              style={styles.input}
              placeholder="Mínimo 6 caracteres"
              autoFocus
            />
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Confirmar Contraseña</label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              minLength={6}
              style={styles.input}
              placeholder="Repite tu contraseña"
            />
          </div>

          {formData.newPassword && formData.confirmPassword &&
           formData.newPassword !== formData.confirmPassword && (
            <div style={styles.error}>
              Las contraseñas no coinciden
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            style={{
              ...styles.button,
              ...(isLoading ? styles.buttonDisabled : {})
            }}
          >
            {isLoading ? 'Restableciendo...' : 'Restablecer Contraseña'}
          </button>
        </form>

        <p style={styles.footer}>
          <Link to="/login" style={styles.link}>
            Volver al inicio de sesión
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
    fontSize: '14px'
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
    display: 'block',
    textAlign: 'center',
    padding: '12px',
    fontSize: '16px',
    fontWeight: '500',
    color: 'white',
    backgroundColor: '#28a745',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    textDecoration: 'none',
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
  error: {
    padding: '10px',
    backgroundColor: '#f8d7da',
    color: '#721c24',
    border: '1px solid #f5c6cb',
    borderRadius: '4px',
    fontSize: '14px'
  },
  successIcon: {
    fontSize: '64px',
    textAlign: 'center',
    marginBottom: '20px',
    color: '#28a745'
  }
};

export default ResetPasswordPage;
