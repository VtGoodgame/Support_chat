def setup_logging():
    try:
        # Получаем абсолютный путь к директории проекта
        project_path = Path(__file__).parent.parent
        
        # Создаем папку logs в директории проекта
        log_dir = project_path / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        # Основной файл для логов
        log_file = log_dir / 'allLog.log'
        
        # Настройка формата логов
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)
        
        # Настройка обработчиков
        handlers = [
            RotatingFileHandler(
                filename=str(log_file),  # Явное преобразование Path в строку
                maxBytes=5 * 1024 * 1024,  # 5 MB
                backupCount=3,
                encoding='utf-8'
            )
        ]
        
        # Добавляем вывод в консоль только если не заморожено (не exe)
        if not getattr(sys, 'frozen', False):
            handlers.append(logging.StreamHandler())
        
        # Базовые настройки логирования
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=handlers
        )
        
        # Устанавливаем формат для всех обработчиков
        for handler in logging.root.handlers:
            handler.setFormatter(formatter)
        
        logger = logging.getLogger(__name__)
        logger.info("Logging setup complete")
        return logger
    
    except Exception as e:
        print(f"Failed to setup logging: {e}", file=sys.stderr)
        raise

# Инициализация логирования
logger = setup_logging()