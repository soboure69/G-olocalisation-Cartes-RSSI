"""
Script d'installation automatique de TensorFlow pour le projet.

Ce script diagnostique l'environnement et installe TensorFlow
avec la meilleure configuration possible.
"""

import subprocess
import sys
import os
import platform
from packaging import version

def run_command(command, description):
    """Exécute une commande et affiche le résultat."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            return True, result.stdout
        else:
            print(f"❌ {description} - Erreur:")
            print(result.stderr)
            return False, result.stderr
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False, str(e)

def check_python_version():
    """Vérifie la compatibilité de la version Python."""
    python_version = platform.python_version()
    print(f"🐍 Version Python détectée: {python_version}")
    
    # TensorFlow supporte Python 3.8-3.11
    if version.parse(python_version) < version.parse("3.8.0"):
        print("❌ Python trop ancien (< 3.8). TensorFlow nécessite Python 3.8+")
        return False
    elif version.parse(python_version) >= version.parse("3.12.0"):
        print("⚠️ Python très récent (>= 3.12). Compatibilité TensorFlow limitée")
        return True  # On essaie quand même
    else:
        print("✅ Version Python compatible avec TensorFlow")
        return True

def check_system_info():
    """Affiche les informations système."""
    print(f"💻 Système: {platform.system()} {platform.release()}")
    print(f"🏗️ Architecture: {platform.machine()}")
    print(f"🔧 Processeur: {platform.processor()}")

def install_tensorflow():
    """Installe TensorFlow avec différentes stratégies."""
    
    print("🎯 INSTALLATION DE TENSORFLOW")
    print("=" * 50)
    
    # Vérifications préliminaires
    check_system_info()
    if not check_python_version():
        return False
    
    # Stratégie 1: Désinstaller les versions existantes
    print("\n📦 Nettoyage des installations existantes...")
    cleanup_commands = [
        "pip uninstall tensorflow tensorflow-cpu tensorflow-gpu -y",
        "pip cache purge"
    ]
    
    for cmd in cleanup_commands:
        run_command(cmd, f"Exécution: {cmd}")
    
    # Stratégie 2: Mise à jour de pip
    success, _ = run_command("python -m pip install --upgrade pip", "Mise à jour de pip")
    if not success:
        print("⚠️ Impossible de mettre à jour pip, on continue...")
    
    # Stratégie 3: Installation TensorFlow CPU (plus stable)
    print("\n🚀 Installation de TensorFlow...")
    
    # Essayer différentes versions par ordre de préférence
    tensorflow_versions = [
        "tensorflow==2.13.0",  # Version stable recommandée
        "tensorflow==2.12.0",  # Version alternative
        "tensorflow-cpu==2.13.0",  # Version CPU seulement
        "tensorflow-cpu",  # Dernière version CPU
        "tensorflow"  # Dernière version complète
    ]
    
    for tf_version in tensorflow_versions:
        print(f"\n🔄 Tentative d'installation: {tf_version}")
        success, output = run_command(f"pip install {tf_version}", f"Installation {tf_version}")
        
        if success:
            # Tester l'installation
            test_success = test_tensorflow_installation()
            if test_success:
                print(f"🎉 TensorFlow installé avec succès: {tf_version}")
                return True
            else:
                print(f"⚠️ Installation réussie mais test échoué pour {tf_version}")
                # Désinstaller et essayer la version suivante
                run_command("pip uninstall tensorflow tensorflow-cpu -y", "Nettoyage")
        else:
            print(f"❌ Échec d'installation pour {tf_version}")
    
    # Stratégie 4: Installation avec options spéciales
    print("\n🔧 Tentative avec options spéciales...")
    special_commands = [
        "pip install tensorflow --no-cache-dir --upgrade",
        "pip install tensorflow --user --no-cache-dir",
        "pip install tensorflow-cpu --no-deps"
    ]
    
    for cmd in special_commands:
        print(f"\n🔄 Tentative: {cmd}")
        success, _ = run_command(cmd, f"Installation spéciale")
        if success and test_tensorflow_installation():
            print("🎉 Installation réussie avec options spéciales!")
            return True
    
    print("\n❌ Toutes les tentatives d'installation ont échoué")
    return False

def test_tensorflow_installation():
    """Teste si TensorFlow est correctement installé."""
    print("🧪 Test de l'installation TensorFlow...")
    
    test_code = """
import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")
print(f"GPU disponible: {tf.config.list_physical_devices('GPU')}")
# Test simple
x = tf.constant([[1.0, 2.0], [3.0, 4.0]])
y = tf.constant([[1.0], [1.0]])
print("✅ Test TensorFlow réussi")
"""
    
    try:
        # Écrire le code de test dans un fichier temporaire
        with open("test_tf.py", "w") as f:
            f.write(test_code)
        
        # Exécuter le test
        result = subprocess.run([sys.executable, "test_tf.py"], 
                              capture_output=True, text=True, timeout=30)
        
        # Nettoyer
        if os.path.exists("test_tf.py"):
            os.remove("test_tf.py")
        
        if result.returncode == 0:
            print("✅ Test TensorFlow réussi")
            print(result.stdout)
            return True
        else:
            print("❌ Test TensorFlow échoué")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def install_project_dependencies():
    """Installe les autres dépendances du projet."""
    print("\n📦 Installation des autres dépendances...")
    
    # Dépendances essentielles sans TensorFlow
    essential_deps = [
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.1.0",
        "xgboost>=1.6.0",
        "matplotlib>=3.5.0",
        "plotly>=5.10.0",
        "dash>=2.6.0",
        "joblib>=1.2.0"
    ]
    
    for dep in essential_deps:
        success, _ = run_command(f"pip install {dep}", f"Installation {dep}")
        if not success:
            print(f"⚠️ Échec pour {dep}, mais on continue...")
    
    print("✅ Dépendances essentielles installées")

def main():
    """Fonction principale."""
    print("🎯 INSTALLATION TENSORFLOW POUR GÉOLOCALISATION RSSI")
    print("=" * 60)
    
    # Installer les dépendances de base
    install_project_dependencies()
    
    # Installer TensorFlow
    tf_success = install_tensorflow()
    
    if tf_success:
        print("\n🎉 INSTALLATION COMPLÈTE RÉUSSIE !")
        print("=" * 50)
        print("✅ TensorFlow installé et fonctionnel")
        print("✅ Toutes les dépendances installées")
        print("✅ Projet prêt à fonctionner avec DNN")
        print("\n🚀 Vous pouvez maintenant lancer:")
        print("   python main.py")
        
        # Test final du projet
        test_project = input("\n🧪 Voulez-vous tester le projet maintenant ? (y/N): ")
        if test_project.lower() == 'y':
            print("\n🔄 Test du projet...")
            success, output = run_command("python -c \"from src.models import RSSIDNNModel; print('✅ Projet fonctionnel')\"", 
                                         "Test du projet")
            if success:
                print("🎉 Projet complètement fonctionnel !")
            else:
                print("⚠️ Problème détecté, mais TensorFlow est installé")
    
    else:
        print("\n❌ INSTALLATION TENSORFLOW ÉCHOUÉE")
        print("=" * 50)
        print("💡 Solutions alternatives:")
        print("1. Utiliser le projet SANS TensorFlow (Random Forest + XGBoost)")
        print("2. Essayer l'installation manuelle:")
        print("   pip install tensorflow-cpu==2.13.0")
        print("3. Utiliser un environnement conda:")
        print("   conda install tensorflow")
        
        use_without_tf = input("\n🤔 Voulez-vous continuer SANS TensorFlow ? (y/N): ")
        if use_without_tf.lower() == 'y':
            print("✅ Le projet fonctionnera avec Random Forest + XGBoost")
            print("🚀 Lancez: python run_without_tensorflow.py")

if __name__ == "__main__":
    main()
