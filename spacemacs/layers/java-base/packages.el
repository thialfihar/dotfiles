(setq java-base-packages
      '(
        ggtags
        helm-gtags
        (java-mode :location built-in)
        ))

(defun java-base/post-init-ggtags ()
  (add-hook 'java-mode-local-vars-hook #'spacemacs/ggtags-mode-enable))

(defun java-base/post-init-helm-gtags ()
  (spacemacs/helm-gtags-define-keys-for-mode 'java-mode))


(defun java-base/init-java-mode ()
  )
