# Migration Plan: PyPI API Tokens to Trusted Publisher

## Current Situation

PyPI has sent a warning about using an API token (`first-api-token`) to publish packages, even though the project has a Trusted Publisher configured. Trusted Publisher (OIDC-based publishing) is the recommended and more secure method.

**Current Setup:**
- GitHub Actions workflow exists at `.github/workflows/publish.yml`
- Workflow uses API tokens stored in secrets:
  - `PYPI_API_TOKEN` for production PyPI
  - `TESTPYPI_API_TOKEN` for test PyPI
- Workflow already has `id-token: write` permission configured (required for OIDC)

## Why Trusted Publisher is Better

1. **More Secure**: No long-lived tokens that can be compromised
2. **No Token Management**: GitHub automatically handles authentication via OIDC
3. **PyPI Recommended**: Official recommendation from PyPI
4. **Simpler**: Fewer secrets to manage

## Migration Steps

### Step 1: Update GitHub Actions Workflow

Modify `.github/workflows/publish.yml`:

**Remove these lines:**
- Lines 71-72: `user: __token__` and `password: ${{ secrets.TESTPYPI_API_TOKEN }}`
- Lines 81-82: `user: __token__` and `password: ${{ secrets.PYPI_API_TOKEN }}`

**Keep:**
- Line 26: `id-token: write` permission (required for OIDC)

The `pypa/gh-action-pypi-publish@release/v1` action will automatically use OIDC authentication when no credentials are provided.

### Step 2: Verify PyPI Trusted Publisher Configuration

1. Go to https://pypi.org/manage/project/slack-blocks-markdown/settings/publishing/
2. Verify the Trusted Publisher is configured with:
   - **Owner**: `atacan`
   - **Repository name**: `slack-blocks-markdown`
   - **Workflow name**: `publish.yml`
   - **Environment name**: Leave empty (or set if using environments)

### Step 3: Remove API Token from PyPI

1. Go to https://pypi.org/manage/account/token/
2. Find the token named `first-api-token`
3. Click "Remove token"
4. Confirm deletion

### Step 4: Remove GitHub Secrets (Optional)

After successful migration, clean up unused secrets:

1. Go to https://github.com/atacan/slack-blocks-markdown/settings/secrets/actions
2. Delete `PYPI_API_TOKEN` (no longer needed)
3. Keep `TESTPYPI_API_TOKEN` if you want to continue using it for test publishing, or set up Trusted Publisher for TestPyPI as well

### Step 5: Test the Migration

**Option A: Test with TestPyPI first**
1. Create a test tag: `git tag v0.1.3-test1`
2. Modify workflow temporarily to publish test builds to TestPyPI
3. Verify OIDC authentication works

**Option B: Test with next real release**
1. When ready for next release (v0.1.4), push the tag
2. Monitor GitHub Actions workflow run
3. Verify successful publication to PyPI

## Expected Workflow Changes

### Before (Using API Tokens)
```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    user: __token__
    password: ${{ secrets.PYPI_API_TOKEN }}
    repository-url: https://upload.pypi.org/legacy/
    print-hash: true
```

### After (Using Trusted Publisher)
```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://upload.pypi.org/legacy/
    print-hash: true
```

## Troubleshooting

### If Publishing Fails After Migration

1. **Check Trusted Publisher Configuration**: Ensure repository name and workflow name match exactly
2. **Verify Permissions**: Ensure `id-token: write` is in workflow permissions
3. **Check PyPI Project Settings**: Verify Trusted Publisher is enabled for the project
4. **Review Workflow Logs**: Look for OIDC authentication errors in GitHub Actions

### Rollback Plan

If issues occur, you can temporarily rollback:
1. Re-add API token credentials to workflow
2. Push a fix
3. Investigate Trusted Publisher configuration
4. Try migration again

## Timeline

- **Immediate**: Review and update workflow file
- **Within 24 hours**: Remove API token from PyPI
- **Next release**: Verify Trusted Publisher works correctly

## References

- [PyPI Trusted Publishers Guide](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [pypa/gh-action-pypi-publish Documentation](https://github.com/pypa/gh-action-pypi-publish)

## Notes

- The warning was triggered because v0.1.3 was published using the API token
- Future releases will use Trusted Publisher once migration is complete
- No changes needed to `pyproject.toml` or package code
