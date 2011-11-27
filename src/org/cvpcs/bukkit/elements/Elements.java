package org.cvpcs.bukkit.elements;

import org.bukkit.plugin.java.JavaPlugin;

import java.util.logging.Logger;

public class Elements extends JavaPlugin {

    private static final Logger LOG = Logger.getLogger("Minecraft");

    public void onDisable() {
    	LOG.info("unloaded!");
    }

    public void onEnable() {
        LOG.info(getDescription().getName() + " v" + getDescription().getVersion() + " loaded!");
    }
}


