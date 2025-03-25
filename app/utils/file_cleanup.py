import os
import tempfile
import threading
import time
import atexit

class FileCleanupManager:
    def __init__(self):
        self.files_to_cleanup = []
        self.cleanup_lock = threading.Lock()
        # Start a background thread to clean up files
        self.cleanup_thread = threading.Thread(target=self._cleanup_thread, daemon=True)
        self.cleanup_thread.start()
        # Register cleanup on exit
        atexit.register(self.cleanup_all)
    
    def mark_for_cleanup(self, filepath):
        """
        Mark a file for deferred cleanup
        """
        if filepath and os.path.exists(filepath):
            with self.cleanup_lock:
                self.files_to_cleanup.append((filepath, time.time()))
    
    def _cleanup_thread(self):
        """
        Background thread that periodically cleans up files
        """
        while True:
            time.sleep(5)  # Check every 5 seconds
            self._attempt_cleanup()
    
    def _attempt_cleanup(self):
        """
        Try to clean up files marked for deletion
        """
        with self.cleanup_lock:
            current_time = time.time()
            remaining_files = []
            
            for filepath, timestamp in self.files_to_cleanup:
                # Only try to delete files older than 10 seconds
                if current_time - timestamp > 10:
                    try:
                        if os.path.exists(filepath):
                            os.unlink(filepath)
                    except (PermissionError, OSError):
                        # File still in use, keep it in the list
                        remaining_files.append((filepath, timestamp))
                else:
                    # File not old enough yet
                    remaining_files.append((filepath, timestamp))
            
            self.files_to_cleanup = remaining_files
    
    def cleanup_all(self):
        """
        Final cleanup attempt when the application exits
        """
        with self.cleanup_lock:
            for filepath, _ in self.files_to_cleanup:
                try:
                    if os.path.exists(filepath):
                        os.unlink(filepath)
                except:
                    pass

# Singleton instance
file_cleanup = FileCleanupManager()